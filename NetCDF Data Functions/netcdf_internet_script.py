:: python script to download selected files from rda.ucar.edu
::
import sys
import os
import urllib2
import cookielib
::
if (len(sys.argv) != 2):
  print "usage: "+sys.argv[0]+" [-q] password_on_RDA_webserver"
  print "-q suppresses the progress message for each file that is downloaded"
  sys.exit(1)
::
passwd_idx=1
verbose=True
if (len(sys.argv) == 3 and sys.argv[1] == "-q"):
  passwd_idx=2
  verbose=False
::
cj=cookielib.MozillaCookieJar()
opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
::
:: check for existing cookies file and authenticate if necessary
do_authentication=False
if (os.path.isfile("auth.rda.ucar.edu")):
  cj.load("auth.rda.ucar.edu",False,True)
  for cookie in cj:
    if (cookie.name == "sess" and cookie.is_expired()):
      do_authentication=True
else:
  do_authentication=True
if (do_authentication):
  login=opener.open("https://rda.ucar.edu/cgi-bin/login","email=sguo10@uncc.edu&password="+sys.argv[1]+"&action=login")
::
:: save the authentication cookies for future downloads
:: NOTE! - cookies are saved for future sessions because overly-frequent authentication to our server can cause your data access to be blocked
  cj.clear_session_cookies()
  cj.save("auth.rda.ucar.edu",True,True)
::
:: download the data file(s)
listoffiles=["CTRL/2000/wrf2d_d01_CTRL_SNOW_200010-200012.nc","CTRL/2000/wrf2d_d01_CTRL_SNOW_ACC_NC_200010-200012.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_200101-200103.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_ACC_NC_200101-200103.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_200104-200106.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_ACC_NC_200104-200106.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_200107-200109.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_ACC_NC_200107-200109.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_200110-200112.nc","CTRL/2001/wrf2d_d01_CTRL_SNOW_ACC_NC_200110-200112.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_200201-200203.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_ACC_NC_200201-200203.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_200204-200206.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_ACC_NC_200204-200206.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_200207-200209.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_ACC_NC_200207-200209.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_200210-200212.nc","CTRL/2002/wrf2d_d01_CTRL_SNOW_ACC_NC_200210-200212.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_200301-200303.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_ACC_NC_200301-200303.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_200304-200306.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_ACC_NC_200304-200306.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_200307-200309.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_ACC_NC_200307-200309.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_200310-200312.nc","CTRL/2003/wrf2d_d01_CTRL_SNOW_ACC_NC_200310-200312.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_200401-200403.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_ACC_NC_200401-200403.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_200404-200406.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_ACC_NC_200404-200406.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_200407-200409.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_ACC_NC_200407-200409.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_200410-200412.nc","CTRL/2004/wrf2d_d01_CTRL_SNOW_ACC_NC_200410-200412.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_200501-200503.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_ACC_NC_200501-200503.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_200504-200506.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_ACC_NC_200504-200506.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_200507-200509.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_ACC_NC_200507-200509.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_200510-200512.nc","CTRL/2005/wrf2d_d01_CTRL_SNOW_ACC_NC_200510-200512.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_200601-200603.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_ACC_NC_200601-200603.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_200604-200606.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_ACC_NC_200604-200606.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_200607-200609.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_ACC_NC_200607-200609.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_200610-200612.nc","CTRL/2006/wrf2d_d01_CTRL_SNOW_ACC_NC_200610-200612.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_200701-200703.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_ACC_NC_200701-200703.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_200704-200706.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_ACC_NC_200704-200706.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_200707-200709.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_ACC_NC_200707-200709.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_200710-200712.nc","CTRL/2007/wrf2d_d01_CTRL_SNOW_ACC_NC_200710-200712.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_200801-200803.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_ACC_NC_200801-200803.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_200804-200806.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_ACC_NC_200804-200806.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_200807-200809.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_ACC_NC_200807-200809.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_200810-200812.nc","CTRL/2008/wrf2d_d01_CTRL_SNOW_ACC_NC_200810-200812.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_200901-200903.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_ACC_NC_200901-200903.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_200904-200906.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_ACC_NC_200904-200906.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_200907-200909.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_ACC_NC_200907-200909.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_200910-200912.nc","CTRL/2009/wrf2d_d01_CTRL_SNOW_ACC_NC_200910-200912.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_201001-201003.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_ACC_NC_201001-201003.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_201004-201006.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_ACC_NC_201004-201006.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_201007-201009.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_ACC_NC_201007-201009.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_201010-201012.nc","CTRL/2010/wrf2d_d01_CTRL_SNOW_ACC_NC_201010-201012.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_201101-201103.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_ACC_NC_201101-201103.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_201104-201106.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_ACC_NC_201104-201106.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_201107-201109.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_ACC_NC_201107-201109.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_201110-201112.nc","CTRL/2011/wrf2d_d01_CTRL_SNOW_ACC_NC_201110-201112.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_201201-201203.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_ACC_NC_201201-201203.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_201204-201206.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_ACC_NC_201204-201206.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_201207-201209.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_ACC_NC_201207-201209.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_201210-201212.nc","CTRL/2012/wrf2d_d01_CTRL_SNOW_ACC_NC_201210-201212.nc","CTRL/2013/wrf2d_d01_CTRL_SNOW_201301-201303.nc","CTRL/2013/wrf2d_d01_CTRL_SNOW_ACC_NC_201301-201303.nc","CTRL/2013/wrf2d_d01_CTRL_SNOW_201304-201306.nc","CTRL/2013/wrf2d_d01_CTRL_SNOW_ACC_NC_201304-201306.nc","CTRL/2013/wrf2d_d01_CTRL_SNOW_201307-201309.nc","CTRL/2013/wrf2d_d01_CTRL_SNOW_ACC_NC_201307-201309.nc"]
for file in listoffiles:
  #file stuff
  idx=file.rfind("/")
  if (idx > 0):
    ofile=file[idx+1:]
  else:
    ofile=file


  if (verbose):
    sys.stdout.write("downloading "+ofile+"...")
    sys.stdout.flush()
  infile=opener.open("http://rda.ucar.edu/data/ds612.0/"+file)
  outfile=open(ofile,"wb")
  outfile.write(infile.read())
  outfile.close()
  if (verbose):
    sys.stdout.write("done.\n")