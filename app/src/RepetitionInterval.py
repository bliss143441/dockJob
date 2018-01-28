from enum import Enum

badModeException = Exception('Bad Mode')
badNumberOfModeParamaters = Exception('Bad number of paramaters passed to mode')
badParamater = Exception('Bad paramater value')

class ModeType(Enum):
  HOURLY = 1
  DAILY = 2
  ONMON = 2
  ONTUE = 2
  ONWED = 2
  ONTHU = 2
  ONFRI = 2
  ONSAT = 2
  ONSUN = 2
  WEEKDAY = 2	#Same hour and minute each weekday (24 hour clock)				"WEEKDAY:13:39" = Run at 1:39pm each weekday
  WEEKEND = 2	#Same hour and minute each weekend day (24 hour clock)			"WEEKEND:13:39" = Run at 1:39pm each weekend
  MONTHLY = 3	#Same hour and minute each day of the month (24 hour clock)	"MONTHLY:13:39:3" = Run at 1:39pm each 3rd of month
  # params are always minute:hour:day

class RepetitionIntervalClass():
  mode = None;
  minute = -1;
  hour = -1; #hour in 24 hour format
  dayOfMonth = -1; #only used in o nthly mode

  def __init__(self, intervalString):
    if (None == intervalString):
      raise badModeException
    a = intervalString.split(":")
    if (len(a) == 0):
      raise badModeException
    modeType = None
    a[0] = a[0].upper().strip()
    for curModeType in ModeType:
      if (curModeType.name == a[0]):
        modeType = curModeType
    if (None == modeType):
      raise badModeException
    if ((1+modeType.value) != len(a)):
      raise badNumberOfModeParamaters
    self.mode = modeType
    self.minute = a[1].strip()
    if (" " in self.minute):
      raise badParamater
    try:
      self.minute = int(self.minute)
    except ValueError:
      raise badParamater
    if (self.minute < 0):
      raise badParamater
    if (self.minute > 59):
      raise badParamater

    #work out hour
    if (self.mode.value > 1):
      self.hour = a[2].strip()
      if (" " in self.hour):
        raise badParamater
      try:
        self.hour = int(self.hour)
      except ValueError:
        raise badParamater
      if (self.hour < 0):
        raise badParamater
      if (self.hour > 23):
        raise badParamater

    #work out day of month
    if (self.mode.value > 2):
      self.dayOfMonth = a[3].strip()
      if (" " in self.dayOfMonth):
        raise badParamater
      try:
        self.dayOfMonth = int(self.dayOfMonth)
      except ValueError:
        raise badParamater
      if (self.dayOfMonth < 0):
        raise badParamater
      if (self.dayOfMonth > 31):
        raise badParamater

    pass


#public class RepetitionInterval {
#	
#	//Modes
#	//Hourly Mode - 
#	//Daily Mode - 
#	//OnMon Mode - 
#	//OnTue Mode
#	//OnWed Mode
#	//OnThu Mode
#	//OnFri Mode
#	//OnSat Mode
#	//OnSun Mode
#	//Weekday Mode - 
#	//Weekend Mode - Same hour and minute each weekend (24 hour clock)
#	//Monthly Mode - Same Day of Month
#	public enum ModeType {
#		HOURLY(1), 	//Same minute past each hour									"HOURLY:12" = 12 minutes past each hour
#		DAILY(2),	//Same hour and minute each day (24 hour clock)					"DAILY:23:59" = Run at 11:59pm each night
#		ONMON(2),	//Same hour and minute each monday (24 hour clock)				"ONMON:23:59" = Run at 11:59pm each monday
#		ONTUE(2),	
#		ONWED(2),	
#		ONTHU(2),	
#		ONFRI(2),	
#		ONSAT(2),	
#		ONSUN(2),	
#		WEEKDAY(2),	//Same hour and minute each weekday (24 hour clock)				"WEEKDAY:13:39" = Run at 1:39pm each weekday
#		WEEKEND(2),	//Same hour and minute each weekend day (24 hour clock)			"WEEKEND:13:39" = Run at 1:39pm each weekend
#		MONTHLY(3)	//Same hour and minute each day of the month (24 hour clock)	"MONTHLY:13:39:3" = Run at 1:39pm each 3rd of month
#		;
#		
#		private int m_numParams;
#		private ModeType(int p_numParams) {
#			m_numParams = p_numParams;
#		}
#		public int getNumParams() {return m_numParams;};
#	}	
#	
#	private ModeType m_mode = null;
#	private int m_minute = -1;
#	private int m_hour = -1; //hour in 24 hour format
#	private int m_day_of_month = -1; //only used in o nthly mode
#	
#	public RepetitionInterval(String p_intervalSTR) throws Exception {
#		if (p_intervalSTR==null) throw new Exception("Bad Mode");
#		if (p_intervalSTR.equals("NULL")) throw new Exception("Bad Mode (NULL)");
#		p_intervalSTR = p_intervalSTR.trim().toUpperCase();

#		String[] arr = p_intervalSTR.split(":");
#		
#		try {
#			m_mode = ModeType.valueOf(arr[0].trim());
#		} catch (Exception e) {
#			e.printStackTrace();
#			throw new Exception("Invalid Mode - " + m_mode + " - " + p_intervalSTR);
#		}
#		if (m_mode==null) throw new Exception("Bad Mode");
#		if (arr.length!=(m_mode.getNumParams()+1)) throw new Exception("Bad number of mode paramaters");
#		
#		switch (m_mode) {
#			case HOURLY:
#				m_minute = Integer.parseInt(arr[1].trim());
#				break;
#			case MONTHLY:
#				m_hour = Integer.parseInt(arr[1].trim());
#				m_minute = Integer.parseInt(arr[2].trim());
#				m_day_of_month = Integer.parseInt(arr[3].trim());
#			default:
#				//All modes that take 2 params have same form: hour:minute
#				m_hour = Integer.parseInt(arr[1].trim());
#				m_minute = Integer.parseInt(arr[2].trim());
#				break;
#		}
#		//ALL modes have minute
#		if (m_minute<0) throw new Exception("Invalid minute");
#		if (m_minute>59) throw new Exception("Invalid minute");
#		
#		
#		//All modes except hourly have hour
#		if (m_mode!=ModeType.HOURLY) {
#			if (m_hour<0) throw new Exception("Invalid hour");
#			if (m_hour>23) throw new Exception("Invalid hour");			
#		}
#		
#		//Only MONTHLY mode has day_of_month
#		if (m_mode==ModeType.MONTHLY) {
#			if (m_day_of_month<1) throw new Exception("Invalid Day Of Month");
#			if (m_day_of_month>31) throw new Exception("Invalid Day Of Month");
#		}
#	}
#	
#	
#	
#	public Date getNextDate() throws Exception {
#		return getNextDate(new Date());
#	}
#	
#	/*
#	 * Return true is the date in the calendar is a day in the pattern
#	 * e.g. ONMON called on a monday returns true if it's a monday
#	 */
#	private boolean isCorrectDay(Calendar p_cal) throws Exception {
#		//Return true if the day in the calendar is the correct day
#		if (m_mode==ModeType.HOURLY) return true; //this path is never used
#		if (m_mode==ModeType.MONTHLY) throw new Exception("Function used where it wasn't designed to be used");
#		
#		if (m_mode==ModeType.DAILY) return equals(p_cal.get(Calendar.DAY_OF_MONTH)==m_day_of_month);
#		
#		int dow = p_cal.get(Calendar.DAY_OF_WEEK);
#		
#		if (m_mode==ModeType.WEEKEND) {
#			if (dow == Calendar.SATURDAY) return true;
#			if (dow == Calendar.SUNDAY) return true;
#			return false;
#		}
#		if (m_mode==ModeType.WEEKDAY) {
#			if (dow == Calendar.MONDAY) return true;
#			if (dow == Calendar.TUESDAY) return true;
#			if (dow == Calendar.WEDNESDAY) return true;
#			if (dow == Calendar.THURSDAY) return true;
#			if (dow == Calendar.FRIDAY) return true;
#			return false;
#		}
#		if (m_mode==ModeType.ONMON) return (dow == Calendar.MONDAY);
#		if (m_mode==ModeType.ONTUE) return (dow == Calendar.TUESDAY);
#		if (m_mode==ModeType.ONWED) return (dow == Calendar.WEDNESDAY);
#		if (m_mode==ModeType.ONTHU) return (dow == Calendar.THURSDAY);
#		if (m_mode==ModeType.ONFRI) return (dow == Calendar.FRIDAY);
#		if (m_mode==ModeType.ONSAT) return (dow == Calendar.SATURDAY);
#		if (m_mode==ModeType.ONSUN) return (dow == Calendar.SUNDAY);
#		
#		throw new Exception("Should never get here");
#	}
#	
#	public Date getNextDate(Date m_from) throws Exception {
#		//Based on the date get next date based on interval
#		Calendar calFromNoSec = Calendar.getInstance();
#		calFromNoSec.setTime(m_from);
#		calFromNoSec.set(Calendar.SECOND, 0);

#		Calendar cal = Calendar.getInstance();
#		cal.setTime(m_from);
#		cal.set(Calendar.SECOND, 0);
#		cal.set(Calendar.MINUTE, m_minute);
#	
#		if (m_mode==ModeType.HOURLY) {
#			if ((cal.getTime().before(calFromNoSec.getTime())) || (cal.getTime().equals(calFromNoSec.getTime()))) {
#				cal.add(Calendar.HOUR_OF_DAY, 1);
#			}
#			return cal.getTime();
#		}

#		cal.set(Calendar.HOUR_OF_DAY, m_hour);
#		if (m_mode.getNumParams()==2) {
#			//Daily based interval - same time every day

#			if (m_mode==ModeType.DAILY) {
#				if ((cal.getTime().before(calFromNoSec.getTime())) || (cal.getTime().equals(calFromNoSec.getTime()))) {
#					cal.add(Calendar.DAY_OF_MONTH, 1);
#				}				
#				return cal.getTime();
#			}
#			
#			//If cur day is the required day then we need to return this day or next one depending on the time
#			if (isCorrectDay(cal)) {
#				if (!(cal.getTime().before(calFromNoSec.getTime())) || (cal.getTime().equals(calFromNoSec.getTime()))) {
#					return cal.getTime();
#				}
#			}
#			//Otherwise return next day that is the current day.
#			for (int c=0;c<8;c++) {
#				cal.add(Calendar.DAY_OF_MONTH, 1);
#				if (isCorrectDay(cal)) return cal.getTime();
#			}
#			throw new Exception("Error - cycled through a week but still didn't match!!!");
#			
#		}

#		//Only MONTHLY mode left
#		cal.set(Calendar.DAY_OF_MONTH, m_day_of_month);
#		if ((cal.getTime().before(m_from)) || (cal.getTime().equals(calFromNoSec.getTime()))) {
#			cal.add(Calendar.MONTH, 1);
#		}
#		
#		
#		return cal.getTime();
#	}
#	
#	public String toString() {
#		String ret = m_mode.toString() + ":";
#		if (m_mode == ModeType.HOURLY) return ret + Integer.toString(m_minute).trim();
#		ret += Integer.toString(m_hour).trim() + ":" + Integer.toString(m_minute).trim();
#		if (m_mode == ModeType.MONTHLY) ret += ":" + Integer.toString(m_day_of_month).trim();
#		return ret;
#	}
#	
#	public boolean equals(RepetitionInterval p_oth) throws Exception {
#		if (p_oth.m_mode!=m_mode) return false;
#		if (p_oth.m_minute!=m_minute) return false;
#		if (p_oth.m_hour!=m_hour) return false;
#		if (p_oth.m_day_of_month!=m_day_of_month) return false;
#		return true;
#	}
#	
#	public static String RepetitionIntervalOutputString(RepetitionInterval p_obj) {
#		if (p_obj==null) return "NULL";
#		return p_obj.toString();
#	}
#	public static RepetitionInterval getRepetitionIntervalInputString(String p_inp) throws Exception {
#		if (p_inp.equals("NULL")) return null;
#		return new RepetitionInterval(p_inp);
#	}

#}
