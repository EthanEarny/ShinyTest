# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from __future__ import division
from mixpanel_api import Mixpanel
import datetime
try:
    import ujson as json
except ImportError:
    import json
from tabulate import tabulate
import pandas as pd
 

def scripter (ymd, script1, script3, script5): #function to combine string querry based on date 

    script2= script1+ymd

    script4= script2+script3+ymd

    script= script4 + script5
    return script

def DoD (newer, older):
    DoD=str(round(((newer-older) / older),3)*100)+'%'
    return DoD

def ConversionRate (first, second):
    ConversionRate = str(round((second / first) ,3)*100)+'%'
    return ConversionRate

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'black'
    return 'color: %s' % color
    
now = datetime.datetime.now()


ymd= " '" + str(now.year) + '-' + str(now.month) + '-' + str(now.day-1) + "'"

ymd2d= " '" + str(now.year) + '-' + str(now.month) + '-' + str(now.day-2) + "'"


mixpanel = Mixpanel('976d8a0ffb18baa7393d37cabdd1c85a')

script1= '''

/* ==========================================================
 * Funnel analysis
 *
 * Simple funnel analysis, ignoring reordering or conversion windows.
 */
var funnel = params.funnel || ["Screen View", "Sign In successful - Yahoo", "Link Amazon button pressed", "Link Amazon successful"];

function main() {
 return Events({
    from_date:'''

script3= ''',
    to_date:  '''

script5=  ''',
    event_selectors: [{event: "Screen View", 
                        selector: '(properties["Screen"] == "Yahoo Amazon") and (properties["$os"] == "Android")'},
                      {event: "Sign In successful - Yahoo",
                        selector: '(properties["$os"] == "Android")'
                      },
                      {event: "Link Amazon button pressed"},
                      {event: "Link Amazon successful"}]
                      
  })
  // get the number of steps completed by each user
  .groupByUser(function(steps_completed, events) {
    steps_completed = steps_completed || 0;
    _.each(events, function(e) {
      if (e.name === funnel[steps_completed]) {
        steps_completed++;
      }
    });
    return steps_completed;
  })
  // filter out users who did not enter the funnel
  .filter(function(item) { return item.value > 0 })
  // Add counts for step N to counts for previous steps.
  // This converts us from "users who ended at each step"
  // into "users who were ever present at each step".
  .reduce(function(accumulators, users_with_final_steps) {
    var funnel_steps = new Array(funnel.length).fill(0);
    _.each(users_with_final_steps, function(user) {
      // for each user, count them once per step
      // until the step they ended on
      for (var i = 0; i < user.value; i++) {
        funnel_steps[i]++;
      }
    });
    // handle previous funnel step counts, if
    // there have been multiple invocations of this function
    _.each(accumulators, function(accumulator) {
      _.each(accumulator, function(step_count, i) {
        funnel_steps[i] += step_count;
      });
    });

    var finalObject = {}
    Object.assign(finalObject, funnel_steps);
    return finalObject;
    
  })
  .map(function(item) {
    return {
    "Screen View": item[0],
    "Sign In Successful - Yahoo" : item[1],
    "Link Amazon button pressed" : item[2],
    "Link Amazon successful" : item[3]
    }
  })
}
'''


YestScript= scripter (ymd, script1, script3, script5)

script2d= scripter (ymd2d, script1, script3, script5)


script1AS= '''

/* ==========================================================
 * Funnel analysis
 *
 * Simple funnel analysis, ignoring reordering or conversion windows.
 */
var funnel = params.funnel || ["Link Amazon button pressed", "Link Amazon successful"];

function main() {
 return Events({
    from_date:'''

script5AS = ''',
event_selectors: [
                      {event: "Link Amazon button pressed"},
                      {event: "Link Amazon successful"}]
                      
  })
  // get the number of steps completed by each user
  .groupByUser(function(steps_completed, events) {
    steps_completed = steps_completed || 0;
    _.each(events, function(e) {
      if (e.name === funnel[steps_completed]) {
        steps_completed++;
      }
    });
    return steps_completed;
  })
  // filter out users who did not enter the funnel
  .filter(function(item) { return item.value > 0 })
  // Add counts for step N to counts for previous steps.
  // This converts us from "users who ended at each step"
  // into "users who were ever present at each step".
  .reduce(function(accumulators, users_with_final_steps) {
    var funnel_steps = new Array(funnel.length).fill(0);
    _.each(users_with_final_steps, function(user) {
      // for each user, count them once per step
      // until the step they ended on
      for (var i = 0; i < user.value; i++) {
        funnel_steps[i]++;
      }
    });
    // handle previous funnel step counts, if
    // there have been multiple invocations of this function
    _.each(accumulators, function(accumulator) {
      _.each(accumulator, function(step_count, i) {
        funnel_steps[i] += step_count;
      });
    });

    var finalObject = {}
    Object.assign(finalObject, funnel_steps);
    return finalObject;
    
  })
  .map(function(item) {
    return {
    "Link Amazon button pressed" : item[0],
    "Link Amazon successful" : item[1]
    }
  })
}


'''

scriptAS= scripter(ymd, script1AS, script3,script5AS)

script1CCPP= '''

/* ==========================================================
 * Funnel analysis
 *
 * Simple funnel analysis, ignoring reordering or conversion windows.
 */
var funnel = params.funnel || ["Link Ccpp button pressed", "Link Ccpp successful"];

function main() {
 return Events({
    from_date:'''
    
script5CCPP=''',
event_selectors: [
                      {event: "Link Ccpp button pressed"},
                      {event: "Link Ccpp successful"}]
                      
  })
  // get the number of steps completed by each user
  .groupByUser(function(steps_completed, events) {
    steps_completed = steps_completed || 0;
    _.each(events, function(e) {
      if (e.name === funnel[steps_completed]) {
        steps_completed++;
      }
    });
    return steps_completed;
  })
  // filter out users who did not enter the funnel
  .filter(function(item) { return item.value > 0 })
  // Add counts for step N to counts for previous steps.
  // This converts us from "users who ended at each step"
  // into "users who were ever present at each step".
  .reduce(function(accumulators, users_with_final_steps) {
    var funnel_steps = new Array(funnel.length).fill(0);
    _.each(users_with_final_steps, function(user) {
      // for each user, count them once per step
      // until the step they ended on
      for (var i = 0; i < user.value; i++) {
        funnel_steps[i]++;
      }
    });
    // handle previous funnel step counts, if
    // there have been multiple invocations of this function
    _.each(accumulators, function(accumulator) {
      _.each(accumulator, function(step_count, i) {
        funnel_steps[i] += step_count;
      });
    });

    var finalObject = {}
    Object.assign(finalObject, funnel_steps);
    return finalObject;
    
  })
  .map(function(item) {
    return {
    "Link Ccpp button pressed" : item[0],
    "Link Ccpp successful" : item[1]
    }
  })
}'''
    
scriptCCPP = scripter (ymd,script1CCPP,script3, script5CCPP )


CCPPSuccess=mixpanel.query_jql(scriptCCPP)
CCPPSuccess=CCPPSuccess[0]
CCPPpercentage= ConversionRate(CCPPSuccess["Link Ccpp button pressed"], CCPPSuccess["Link Ccpp successful"])
CCPPSuccess= {'Link CCPP Successful' : [CCPPpercentage]}
dfCCPP=pd.DataFrame.from_dict(CCPPSuccess, orient='index', columns = ['Success Rate'] )
pd.DataFrame.to_csv(dfCCPP, '/Users/ethanhaik/Desktop/test.csv')




#print pd.DataFrame.to_html(dfCCPP)



Amazonsuccess= mixpanel.query_jql(scriptAS)
Amazonsuccess=Amazonsuccess[0]
Amazonpercentage= ConversionRate (Amazonsuccess ['Link Amazon button pressed'], Amazonsuccess['Link Amazon successful'])  
Amzsuccess= {'Link Amazon Succesful' : [Amazonpercentage]}
dfas=pd.DataFrame.from_dict(Amzsuccess, orient='index', columns = ['Success Rate'] )
#print pd.DataFrame.to_html(dfas)



yesterday = mixpanel.query_jql(YestScript)
yesterday= yesterday[0]
twodays= mixpanel.query_jql(script2d)
twodays=twodays[0]


table= {}
table ['Screen View']= yesterday['Screen View']
table ['Screen View DoD']=DoD (yesterday['Screen View'], twodays['Screen View']) 
table ['Sign In Successful - Yahoo'] = yesterday ['Sign In Successful - Yahoo']
table ['App Download Conversion Rate'] = ConversionRate (yesterday [ 'Screen View'], yesterday ['Sign In Successful - Yahoo'])
table ['Sign in Succesful DoD'] = DoD (yesterday['Sign In Successful - Yahoo'],twodays['Sign In Successful - Yahoo'])
table ['Link Amazon button pressed']= yesterday [ 'Link Amazon button pressed']
table ['Amazon button pressed conversion rate'] = ConversionRate (yesterday [ 'Sign In Successful - Yahoo'], yesterday ['Link Amazon button pressed'])
table ['Link Amazon button pressed DoD'] = DoD (yesterday['Link Amazon button pressed'], twodays['Link Amazon button pressed'])
table ['Link Amazon successful'] = yesterday ['Link Amazon successful']
table ['Amazon success rate'] = ConversionRate (yesterday [ 'Link Amazon button pressed'], yesterday ['Link Amazon successful'])
table['Total Conversion Rate'] = table ['Link Amazon successful'] / table['Screen View']

tester = {'AND APP' : [(table ['Screen View']), (table ['Screen View DoD']), (table ['Sign In Successful - Yahoo']), (table['Sign in Succesful DoD']), (table['App Download Conversion Rate']), (table ['Link Amazon button pressed']), (table['Link Amazon button pressed DoD']), (table ['Link Amazon successful']), (table ['Amazon success rate']), table ['Total Conversion Rate']]}


df= pd.DataFrame.from_dict(tester,orient='index', columns = ['Screen View', 'Screen View DoD','Sign In Successful - Yahoo','Sign in Succesful DoD', 'App Download Conversion Rate', 'Link Amazon button pressed', 'Link Amazon button pressed DoD','Link Amazon successful', 'Amazon success rate', 'Total Conversion Rate' ])

#pd.DataFrame.to_csv(df, '/Users/ethanhaik/Desktop/e.csv')
#print pd.DataFrame.to_html(df)



#print tabulate (df, headers=['Screen View', 'Screen View DoD','Sign In Successful - Yahoo','Sign in Succesful DoD', 'App Download Conversion Rate', 'Link Amazon button pressed', 'Link Amazon button pressed DoD','Link Amazon successful', 'Amazon success rate', 'Total Conversion Rate' ])
#print (table)
#print yesterday
 


#s= df.style.applymap(color_negative_red)
#print s.render
#output_file = 'events'+timestamp+'.json'
#open_mode = 'w+'
#with open(output_file, open_mode) as output:
#    json.dump(temp, output)

