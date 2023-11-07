"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  You MUST provide the following two functions
#  with these signatures, so that I can write
#  automated tests for grading.  You must keep
#  these signatures even if you don't use all the
#  same arguments.  Arguments are explained in the
#  javadoc comments.
#



def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    #grab the time
    table = {
    "200": 34,
    "400": 32,
    "600": 30, 
    "1000": 28
    }
    time = arrow.get(brevet_start_time)


    if control_dist_km > brevet_dist_km:
      control_dist_km = brevet_dist_km

    remaining_distance = control_dist_km
    opentime = 0
    save = 0
    leg = 0
    for key, value in table.items():
      leg = int(key) - save
      save = int(key)
      if remaining_distance > leg:
        opentime += leg / value
        remaining_distance -= leg
      else:
        opentime += remaining_distance / value


       
        hours = int(opentime)
        minutes = round((opentime*60) % 60)
        seconds = round((opentime*3600) % 60)
        time = time.shift(hours=hours, minutes = minutes, seconds = seconds)

        return time.isoformat()


      


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    table = {
      "200": 15,
      "400": 15,
      "600": 15, 
      "1000": 11.428
    }
    
   
  
    time = arrow.get(brevet_start_time)


    #special case according to the rules/oddities
    if(control_dist_km == 0):
      time = time.shift(hours=1) 
      return time.isoformat()

    if control_dist_km < 60:
      opentime  = (control_dist_km / 20) +1
      hours = int(opentime)   
      minutes = (opentime*60) % 60  
      seconds = (opentime*3600) % 60  
      time = time.shift(hours=hours, minutes = minutes, seconds = seconds)

      return time.isoformat()
    
    if control_dist_km >= brevet_dist_km:
      
      if(int(brevet_dist_km) == 200):
        time = time.shift(hours = 13, minutes = 30)
        return time.isoformat()
      if(int(brevet_dist_km) == 300):
        time = time.shift(hours = 20)
        return time.isoformat()
      if(int(brevet_dist_km) == 400):
        time = time.shift(hours = 27)
        return time.isoformat()
      if(int(brevet_dist_km) == 600):
        time = time.shift(hours = 40)
        return time.isoformat()
      if(int(brevet_dist_km) == 1000):
        time = time.shift(hours = 75)
        return time.isoformat()

    remaining_distance = control_dist_km
    opentime = 0
    save = 0
    leg = 0
    for key, value in table.items():
      leg = int(key) - save
      save = int(key)
      if remaining_distance > leg:
        opentime += leg / value
        remaining_distance -= leg
      else:
        opentime += remaining_distance / value


      
        hours = int(opentime)
        minutes = (opentime*60) % 60
        seconds = (opentime*3600) % 60
        time = time.shift(hours=hours, minutes = minutes, seconds = seconds)

        return time.isoformat()
    
def main():
  time = arrow.get("2017-01-01T00:00:00+00:00")
  close = arrow.get(close_time(20, 200, time))
  print(close.format("YYYY-MM-DD HH:mm"))
  test = arrow.get(open_time(20, 200, time))
  print(test.format("YYYY-MM-DD HH:mm"))

main()

