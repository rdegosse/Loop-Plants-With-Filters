# Loop-Plants-With-Filters
NO WARRANTY, AS IS, NO SUPPORT... unless you are nice


-- Farmware for farmbot --

Loop plants with filters, execute sequences and save meta data (FARMBOT_OS 6 minimum)


-- Do ---

- Load all plants for current device
- Filter plants with Plant name, Openfarm Slug Name, Plant Age in day range, Meta data key/value
- Sort plants by X,Y
- Execute Init Sequence
- Loop all filtered plants
    - Execute 'Before Move' Sequence
    - Move to plant coordinate (X,Y) withe default Z and default speed
    - Execute 'After Move' Sequence
    - Save meta data key/value
- Execute End Sequence




-- input ---

  {"name": "pointname", "label": "Filter by plant name", "value": "*"},
-> Filter by plant name (equal/Not case sensitive)
-> default : * -> all plant name 
  
  {"name": "openfarm_slug", "label": "Filter by Openfarm slug name", "value": "*"},
-> Filter by Openfarm type (equal/Not case sensitive)
-> default : * -> all openfarm_slug

  {"name": "age_min_day", "label": "Filter by plant age (minimum days)", "value": "-1"},
-> Filter by minimum plant age in days
-> default : -1 -> to be sure with time zone and large range..
  
  {"name": "age_max_day", "label": "Filter by plant age (maximum days)", "value": "36500"},
-> Filter by maximum plant age in days
-> default : 36500 -> a plant of a century...
  
  {"name": "filter_meta_key", "label": "Filter by meta data : key", "value": "None"},
-> Filter by meta data - KEY
-> default : None -> no meta filter
  
  {"name": "filter_meta_value", "label": "Filter by meta data : value", "value": "None"},
-> Filter by meta data - VALUE (equal/Not case sensitive)
-> default : None -> no meta filter

  {"name": "sequence_init", "label": "Init Sequence Name (one time)", "value": "None"},
-> Execute sequence one time, on start. Sequence Name (equal/Not case sensitive)
-> default : None -> no execute sequence

  {"name": "sequence_beforemove", "label": "Sequence name Before Next Move  (each plant)", "value": "None"},
-> Execute sequence before each move. Sequence Name (equal/Not case sensitive)
-> default : None -> no execute sequence
  
  {"name": "sequence_aftermove", "label": "Sequence Name After Move  (each plant)", "value": "None"},
-> Execute sequence after each move. Sequence Name (equal/Not case sensitive)
-> default : None -> no execute sequence

  {"name": "sequence_end", "label": "End Sequence Name (one time)", "value": "None"},
-> Execute sequence one time, at the end. Sequence Name (equal/Not case sensitive)
-> default : None -> no execute sequence

  {"name": "save_meta_key", "label": "Save in meta data : key", "value": "None"},
-> Save meta data after sequence_aftermove - KEY
-> default : None -> no save meta data

  {"name": "save_meta_value", "label": "Save in meta data : value", "value": "None"},
-> Save meta data after sequence_aftermove - VALUE
-> default : None -> no save meta data

  {"name": "default_z", "label": "default Z axis value when moving", "value": 0},
-> default z axis coordinate when moving
-> default : 0 -> Z axis coordinate

  {"name": "default_speed", "label": "default speed value when moving", "value": 800},
-> default speed when moving
-> default : 800 -> default value in celery script

  {"name": "debug", "label": "Debug (0-> No FW debug msg, 1-> FW debug msg, 2-> No Move/exec and FW debug msg only)", "value": 1}
-> debug mode : 0 -> no farmware debug log, 1 -> farmware debug log, 2 -> simulation : no move, no execute sequence, no save meta data AND only farmware debug log
-> default : 1 -> move/exec and debug log


