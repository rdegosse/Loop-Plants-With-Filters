
from FARMWARE import MyFarmware
from CeleryPy import log



if __name__ == "__main__":

    FARMWARE_NAME = "Loop-Plants-With-Filters"

    log('Start...', message_type='info', title=FARMWARE_NAME)
    
    
    try:
        farmware = MyFarmware(FARMWARE_NAME)
    except Exception as e:
        log(e ,message_type='error', title=FARMWARE_NAME + " : init" )
        raise Exception(e)
    else:
        try:
            farmware.run()
        except Exception as e:
            log(e ,message_type='error', title=FARMWARE_NAME + " : run" )
            raise Exception(e)
    

    log('End...', message_type='info', title=FARMWARE_NAME)

