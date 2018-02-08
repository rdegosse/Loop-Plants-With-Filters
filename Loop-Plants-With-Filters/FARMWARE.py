import os
import datetime
from API import API
from CeleryPy import log
from CeleryPy import move_absolute
from CeleryPy import execute_sequence

class MyFarmware():

    def get_input_env(self):
        prefix = self.farmwarename.lower().replace('-','_')
        
        self.input_pointname = os.environ.get(prefix+"_pointname", '*')
        self.input_openfarm_slug = os.environ.get(prefix+"_openfarm_slug", '*')
        self.input_age_min_day = int(os.environ.get(prefix+"_age_min_day", -1))
        self.input_age_max_day = int(os.environ.get(prefix+"_age_max_day", 36500))
        self.input_filter_meta_key = os.environ.get(prefix+"_filter_meta_key", 'None')
        self.input_filter_meta_value = os.environ.get(prefix+"_filter_meta_value", 'None')
        self.input_sequence_init = os.environ.get(prefix+"_sequence_init", 'None')
        self.input_sequence_beforemove  = os.environ.get(prefix+"_sequence_beforemove", 'None')
        self.input_sequence_aftermove = os.environ.get(prefix+"_sequence_aftermove", 'None')
        self.input_sequence_end = os.environ.get(prefix+"_sequence_end", 'None')
        self.input_save_meta_key = os.environ.get(prefix+"_save_meta_key", 'None')
        self.input_save_meta_value = os.environ.get(prefix+"_save_meta_value", 'None')
        self.input_default_z = int(os.environ.get(prefix+"_default_z", 0))
        self.input_default_speed = int(os.environ.get(prefix+"_default_speed", 800))
        self.input_debug = int(os.environ.get(prefix+"_debug", 1))

        if self.input_debug >= 1:
            log('pointname: {}'.format(self.input_pointname), message_type='debug', title=self.farmwarename)
            log('openfarm_slug: {}'.format(self.input_openfarm_slug), message_type='debug', title=self.farmwarename)
            log('age_min_day: {}'.format(self.input_age_min_day), message_type='debug', title=self.farmwarename)
            log('age_max_day: {}'.format(self.input_age_max_day), message_type='debug', title=self.farmwarename)
            log('filter_meta_key: {}'.format(self.input_filter_meta_key), message_type='debug', title=self.farmwarename)
            log('filter_meta_value: {}'.format(self.input_filter_meta_value), message_type='debug', title=self.farmwarename)
            log('sequence_init: {}'.format(self.input_sequence_init), message_type='debug', title=self.farmwarename)
            log('sequence_beforemove: {}'.format(self.input_sequence_beforemove), message_type='debug', title=self.farmwarename)
            log('sequence_aftermove: {}'.format(self.input_sequence_aftermove), message_type='debug', title=self.farmwarename)
            log('sequence_end: {}'.format(self.input_sequence_end), message_type='debug', title=self.farmwarename)
            log('save_meta_key: {}'.format(self.input_save_meta_key), message_type='debug', title=self.farmwarename)
            log('save_meta_value: {}'.format(self.input_save_meta_value), message_type='debug', title=self.farmwarename)
            log('default_z: {}'.format(self.input_default_z), message_type='debug', title=self.farmwarename)
            log('default_speed: {}'.format(self.input_default_speed), message_type='debug', title=self.farmwarename)
            log('debug: {}'.format(self.input_debug), message_type='debug', title=self.farmwarename)
        
    def __init__(self,farmwarename):
        self.farmwarename = farmwarename
        self.get_input_env()
        self.api = API(self)
        self.points = []

    def apply_filters(self, points, point_name='', openfarm_slug='', age_min_day=0, age_max_day=36500, meta_key='', meta_value='', pointer_type='Plant'):
        if self.input_debug >= 1: log(points, message_type='debug', title=str(self.farmwarename) + ' : load_points')
        filtered_points = []
        now = datetime.datetime.utcnow()
        for p in points:
            if p['pointer_type'].lower() == pointer_type.lower():
                b_meta = False
                age_day = (now - datetime.datetime.strptime(p['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')).days
                if str(meta_key).lower() != 'none':
                    try:
                        b_meta = ((p['meta'][meta_key]).lower() == meta_value.lower())
                    except Exception as e:
                        b_meta = False
                else:
                    b_meta = True
                if  (p['name'].lower() == point_name.lower() or point_name == '*') and (p['openfarm_slug'].lower() == openfarm_slug.lower() or openfarm_slug == '*') and (age_min_day <= age_day <= age_max_day) and b_meta==True:
                    filtered_points.append(p.copy())
        return filtered_points

    def load_points_with_filters(self):
        self.points = self.apply_filters(
            points=self.api.api_get('points'),
            point_name=self.input_pointname,
            openfarm_slug=self.input_openfarm_slug,
            age_min_day=self.input_age_min_day,
            age_max_day=self.input_age_max_day,
            meta_key=self.input_filter_meta_key,
            meta_value=self.input_filter_meta_value,
            pointer_type='Plant')
        if self.input_debug >= 1: log(self.points, message_type='debug', title=str(self.farmwarename) + ' : load_points_with_filters')
        

    def sort_points(self):
        self.points = sorted(self.points , key=lambda elem: (int(elem['x']), int(elem['y'])))
        if self.input_debug >= 1: log(self.points, message_type='debug', title=str(self.farmwarename) + ' : sort_points')
        #self.points, self.tab_id = Get_Optimal_Way(self.points)

    def load_sequences_id(self):
        self.sequences = self.api.api_get('sequences')
        self.input_sequence_init_id = -1
        self.input_sequence_beforemove_id = -1
        self.input_sequence_aftermove_id = -1
        self.input_sequence_end_id = -1
        for s in self.sequences:
            if str(s['name']).lower() == self.input_sequence_init.lower() : self.input_sequence_init_id = int(s['id'])
            if str(s['name']).lower() == self.input_sequence_beforemove.lower() : self.input_sequence_beforemove_id = int(s['id'])
            if str(s['name']).lower() == self.input_sequence_aftermove.lower() : self.input_sequence_aftermove_id = int(s['id'])    
            if str(s['name']).lower() == self.input_sequence_end.lower() : self.input_sequence_end_id = int(s['id'])    
        if self.input_debug >= 1:
            log('init: ' + self.input_sequence_init + ' id:' + str(self.input_sequence_init_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
            log('before: ' + self.input_sequence_beforemove + ' id:' + str(self.input_sequence_beforemove_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
            log('after: ' + self.input_sequence_aftermove + ' id:' + str(self.input_sequence_aftermove_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
            log('end: ' + self.input_sequence_end + ' id:' + str(self.input_sequence_end_id), message_type='debug', title=str(self.farmwarename) + ' : load_sequences_id')
    
    def execute_sequence_init(self):
        if self.input_sequence_init_id != -1 :
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_init + ' id:' + str(self.input_sequence_init_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_init')
            if self.input_debug < 2: execute_sequence(sequence_id=self.input_sequence_init_id)
        else:
            if self.input_debug >= 1: log('Sequence Not Found', message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_init')

    def execute_sequence_before(self):
        if self.input_sequence_beforemove_id != -1 : 
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_beforemove + ' id:' + str(self.input_sequence_beforemove_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_before')
            if self.input_debug < 2: execute_sequence(sequence_id=self.input_sequence_beforemove_id)
        else:
            if self.input_debug >= 1: log('Sequence Not Found', message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_before')
                

    def execute_sequence_after(self):
        if self.input_sequence_aftermove_id != -1 : 
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_aftermove + ' id:' + str(self.input_sequence_aftermove_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_after')
            if self.input_debug < 2: execute_sequence(sequence_id=self.input_sequence_aftermove_id)
        else:
            if self.input_debug >= 1: log('Sequence Not Found', message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_after')

    def execute_sequence_end(self):
        if self.input_sequence_end_id != -1 : 
            if self.input_debug >= 1: log('Execute Sequence: ' + self.input_sequence_end + ' id:' + str(self.input_sequence_end_id), message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_end')
            if self.input_debug < 2: execute_sequence(sequence_id=self.input_sequence_end_id)
        else:
            if self.input_debug >= 1: log('Sequence Not Found' , message_type='debug', title=str(self.farmwarename) + ' : execute_sequence_end')

    def move_absolute_point(self,point):
            if self.input_debug >= 1: log('Move absolute: ' + str(point) , message_type='debug', title=str(self.farmwarename) + ' : move_absolute_point')
            if self.input_debug < 2: 
                move_absolute(
                    location=[point['x'],point['y'] ,self.input_default_z],
                    offset=[0, 0, 0],
                    speed=self.input_default_speed)

    def save_meta(self,point):
        if str(self.input_save_meta_key).lower() != 'none':
            if self.input_debug >= 1: log('Save Meta Information: ' + str(point['id']) , message_type='debug', title=str(self.farmwarename) + ' : save_meta')
            if self.input_debug < 2 :
                point['meta'][self.input_save_meta_key]=self.input_save_meta_value
                endpoint = 'points/{}'.format(point['id'])
                self.api.api_put(endpoint=endpoint, data=point)


    def loop_points(self):
        for p in self.points:
            self.execute_sequence_before()
            self.move_absolute_point(p)
            self.execute_sequence_after()
            self.save_meta(p)
    
    
    def run(self):
        self.load_points_with_filters()
        self.sort_points()
        if len(self.points) > 0 : self.load_sequences_id()
        if len(self.points) > 0 : self.execute_sequence_init()        
        if len(self.points) > 0 : self.loop_points()
        if len(self.points) > 0 : self.execute_sequence_end()
        