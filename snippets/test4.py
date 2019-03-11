import dns.resolver #import the module

myResolver = dns.resolver.Resolver() #create a new instance named 'myResolver'
myAnswers = myResolver.query("google.com", "NS") #Lookup the 'A' record(s) for
for rdata in myAnswers.response.additional: #for each response
        print (rdata) #print the data
        
