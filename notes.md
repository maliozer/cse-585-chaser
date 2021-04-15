## map_checker()

- ```static map.is_possible=False```<br>
- ```static map.checktrace= set()```<br>

set root as current position
add root to checktrace
if manhattan_distance equal to 1:
    it is possible
    ```static.is_possinle=True``` <br>
    ```break```

look:
    left
    right
    up
    down

- if(left) then next pos is left as pos | map_checker
- if(right) then next pos is left as pos | map_checker
- if(up) then next pos is left as pos | map_checker
- if(down) then next pos is left as pos | map_checker
