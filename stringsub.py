given_string = "I think %s is a perfectly normal thing to do in public."
def sub1(s):
    return given_string %s

print sub1("running") 
# => "I think running is a perfectly normal thing to do in public."    
print sub1("sleeping") 
# => "I think sleeping is a perfectly normal thing to do in public."


given_string2 = "I think %s and %s are perfectly normal things to do in public."
def sub2(s1, s2):
    return given_string2 %(s1, s2)
    

print sub2("running", "sleeping") 
# => "I think running and sleeping are perfectly normal things to do in public."
print sub2("sleeping", "running") 
# => "I think sleeping and running are perfectly normal things to do in public."

given_string3 = "I'm %(nickname)s. My real name is %(name)s, but my friends call me %(nickname)s."
def sub_m(name, nickname):
    return given_string3 % {"name": name, "nickname": nickname}
    

print sub_m("Mike", "Goose") 
# => "I'm Goose. My real name is Mike, but my friends call me Goose."

def escape_html2(s):
	for (i, o) in (("&", "&amp;"),
					(">", "&gt;"),
					("<", "&lt"),
					('"', "&quot;")):
		s = s.replace(i, o)
	return s
	
import cgi
def escape_html(s):
	return cgi.escape(s, quote = True)
