from pyral import Rally, rallyWorkset
import pandas as pd
import pyaml

class r:
    
    def __init__(self, url, apikey, workspace, project, logging):
        self.rally = Rally(url, apikey=apikey, workspace=workspace, project=project)
        self.project = project
        if logging:
            self.rally.enableLogging('r.log')

    def setFeature(self, reqinfo):
        print ("Setting feature")        
        rallyid = self.rally.put('Feature', reqinfo)
        return rallyid

    def setUserStory(self, reqinfo):
        print ("Setting user story.")
        rallyid = self.rally.put('UserStory', reqinfo)
        return rallyid

    def setTask(self, reqinfo):
        print ("Setting task.")
        rallyid = self.rally.put('Task', reqinfo)
        return rallyid

    def getFeature(self, f_name):
        print ("Getting feature.")

        to_query = 'FormattedID = "' + f_name + '"'
        response = self.rally.get('PortfolioItem',query=to_query)
        if not response.errors:
            for f in response:
                return f

    def getUserStory(self, us_name):
        print ("Getting user story.")

        to_query = 'FormattedID = "' + us_name + '"'
        response = self.rally.get('UserStory',query=to_query)
        if not response.errors:
            for us in response:
                return us

    def getBoard(self, user_fields):
        print ("Getting user stories.")

        project_req = self.rally.get('Project', fetch=True, query='Name = "%s"' % (self.project))
        project = project_req.next()
        user_stories = self.rally.get('HierarchicalRequirement', fetch=True, query='Project = %s' % (project.ref))

        # create dataframe to hold all the user story data
        data = pd.DataFrame()
        
        # standard fields
        default_fields = ["User story number","Feature number","User story name"]

        # add standard fields to dataframe
        for field in default_fields:
            data[field]=""

        # add user fields to dataframe
        for field in user_fields:
            data[field]=""

        # for each user story, get info
        for instance in user_stories:
            us = instance.FormattedID
            feature = instance.Feature
            
            if feature is not None:
                feature = feature.FormattedID
            else:
                feature=""
            
            us_name = instance.Name
            
            addme = {"User story number":us, "Feature number":feature, "User story name":us_name}

            for field in user_fields:
                key = field
                if "." in field:
                    a,b = field.split(".")
                    value = getattr(getattr(instance,a),b)
                else:
                    value = getattr(instance,field)
                addme.update({key:value})

            #examples include: instance.Status, instance.Language, instance.XTMID, instance.RequestedBy

            data = data.append(addme, ignore_index=True)

        return data

    def getTasks(self, us_name):
        print ("Getting tasks.")

        to_query = 'WorkProduct.FormattedID = "' + us_name + '"'
        response = self.rally.get('Task',query=to_query)
        if not response.errors:
            return response
        else:
            print (response.errors)
