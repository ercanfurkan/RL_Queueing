#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 13:43:58 2024

@author: furkancanercan
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 08:41:39 2024
 
@author: 10450
"""
 
#Re-design Object Oriented Simulation Environment for MM1 Queue
#Record important Queue statistics
#Prepare Charts PLots and Tables
#Verify and Validate that it works Correctly
#Prepare the schematics of how it works so your dumb advisors can understand
#Determine a logical objective function with all metrics in the same Unit
 
#https://www.youtube.com/watch?v=d9hpfrrZXac&list=PLU6SqdYcYsfJxRfVS-vKgVa-Oz-THIJNk
# Watch queueing theory
 
 
 
#Extend those above to GI / GI / 1 Queue (very easy)
 
#Extend it to the more than 1 server case
 
#After that is done think about on Production Queue
#Up / Down Times Production Machines and Then 1 Buffer and then another Machine
 
#Watch below videos to do the production bit
#https://www.youtube.com/watch?v=d9hpfrrZXac&list=PLU6SqdYcYsfJxRfVS-vKgVa-Oz-THIJNk
 
 
#The Class to have globally reachable variables for storing
#simulation information
 
import simpy
import numpy as np
import pandas
import plotly.express as px
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
import math
#pio.renderers.default = 'svg'
pio.renderers.default = 'browser'
 
 
class G:
   
    #Model Parameters
    arrival_rate = 1 / 2.0
    service_rate = 1 / 4.0
    simulation_length = 5000
    number_of_runs = 100
    warm_up_period = 0
    num_of_servers = 1
   
    #Store Customer objects
    customers = []
   
    
    #Storing Simulation Statistics
    
    #Record the times when the server is idle
    idle_time = 0
    
    #No queue time record the times when queue length is 0
    
    no_queue_time = 0    
    #Record arrival times
    arrival_time = []
   
    #Record departure times
    departure_time = []
   
    #Record the number in system every time an arrival or departure happens
    num_in_system = []
    
    #Record the times whenever an arrival or departure occurs aka number in system
    #changes
    change_time = []
   
    #Enter queue and exit queue times
    enter_queue = []
    exit_queue = []
   
    #Enter service and exit service times
    enter_serv = []
    exit_serv = []
    
    #Service Time
    serv_time = []
    
    #Record the times whenever the number in queue changes
    change_in_queue = []
   
    #Record the number in queue
    num_in_queue = []
   
    #Record time spent in queue
    queue_time = []
   
    #Record time spent in system
    system_time = []
    
    #Resets the variables so that a new run can be stored
    def reset_stats():
      
        G.customers = []
        G.idle_time = 0
        G.no_queue_time = 0    
        G.arrival_time = []
        G.departure_time = []
        G.num_in_system = []
        G.change_time = []
        G.enter_queue = []
        G.exit_queue = []
        G.enter_serv = []
        G.exit_serv = []
        G.serv_time = []
        G.change_in_queue = []
        G.num_in_queue = []
        G.queue_time = []
        G.system_time = []
        
    
#Class of arriving customers
#Store also arrival time to system,arrival time to queue departure from queue and
#departure from the system
class customer:
    def __init__(self,customer_id):
        self.customer_id = customer_id
        self.system_arrival = 0
        self.enter_queue = 0
        self.exit_queue = 0
        self.enter_service = 0
        self.exit_service = 0
        self.service_time = 0
        self.queue_time = 0
        self.system_departure = 0
        self.system_time = 0
       
class Simulation_Model:
   
    
    #We can add variables to keep track of things
    def __init__(self):
        self.env = simpy.Environment()
        self.customer_number = 0
        self.server = simpy.Resource(self.env,capacity = G.num_of_servers)
        self.num_in_system = 0
        self.num_in_queue = 0
   
    #The main method to start and continue the simulation
    def generate_arrivals(self):
       
        #Run as long as the simulation time exceeds the length
       
        while True:
            #Wait exponential time between arrivals
            wait_time = np.random.exponential(G.arrival_rate)
            #wait_time = G.arrival_rate
            #Freeze the clock and wait
            yield self.env.timeout(wait_time)
           
            #A new patient arrived increase the counter
            #Count the number in system
            #Record the number in system
            self.customer_number+=1
            self.num_in_system+=1
            G.num_in_system.append(self.num_in_system)
            G.change_time.append(self.env.now)
            G.arrival_time.append(self.env.now)
           
            #Create the new patient as the counter naming the patient id
            #Record its arrival
            new_customer = customer(self.customer_number)
            new_customer.system_arrival = self.env.now
            G.customers.append(new_customer)
           
            print("Customer: " + str(new_customer.customer_id) + "arrived at :" + str(self.env.now))
                 
            #Send the customer to the queue of server
            self.env.process(self.serve_customers(new_customer))
           
    def serve_customers(self,customer):
       
        #The customer comes to the beginning of the queue
        #Record the time customer enters the queue
        #Update the number people in queue and record it
        customer.enter_queue = self.env.now
        G.enter_queue.append(self.env.now)
        G.change_in_queue.append(self.env.now)
        self.num_in_queue+=1
        G.num_in_queue.append(self.num_in_queue)
       
        print("Customer: " + str(customer.customer_id) + "entered queue at :" + str(self.env.now))
       
        with self.server.request() as request:
           
            #Wait until the server is free
            yield request
           
            #Continue once the server is free
            customer.exit_queue = self.env.now
            G.exit_queue.append(self.env.now)
            G.enter_serv.append(self.env.now)
            customer.enter_service = self.env.now
            G.change_in_queue.append(self.env.now)
            self.num_in_queue-=1
            G.num_in_queue.append(self.num_in_queue)
            customer.queue_time = customer.exit_queue - customer.enter_queue
            G.queue_time.append(customer.queue_time)
            print("Customer: " + str(customer.customer_id) + "exitted the queue at :" + str(self.env.now))
           
            #Wait exponential time for the service
            service_time = np.random.exponential(G.service_rate)
            
            #service_time = G.service_rate
            yield self.env.timeout(service_time)
           
            print("Customer: " + str(customer.customer_id) + "exitted the the system at :" + str(self.env.now))
            customer.system_departure = self.env.now
            G.departure_time.append(self.env.now)
            G.exit_serv.append(self.env.now)
            customer.exit_service = self.env.now
            customer.service_time = customer.exit_service - customer.enter_service
            G.serv_time.append(customer.service_time)
            self.num_in_system-=1
            G.num_in_system.append(self.num_in_system)
            G.change_time.append(self.env.now)
            customer.system_time = customer.system_departure - customer.system_arrival
            G.system_time.append(customer.system_time)
           
    def run(self):
        self.env.process(self.generate_arrivals())
        self.env.run(until = G.simulation_length)
       
        
    #Number in system Path
    def queue_path_plot(self,plot=True):
        
        #Create a time index to identify the time units passed in queue run
        #What it does it creates unit time indicies to record the times when nothing happened
        #and when times sth happened. E.g in 3.2 sbd came then it creates 0,1,2,3,3.2,4 
        #Time indicies
        time_index = []
        index = 0
        
        #Events with the same logic. It should repeat the previous num in system till it updates
        events = []
        event = 0
        
        for items in range(len(G.change_time)):
            
            while index < G.change_time[items]:
                #Measure the time the system is empty
                time_index.append(index)
                events.append(event)
                index+=1
            event = G.num_in_system[items]
            events.append(event)
            time_index.append(G.change_time[items])
        
        #Also add the last events if nothing happens until the simulation ends
        last_time_event_happend = int(time_index[-1]) + 1
        
        #Add the indicies and plus since nothing happend repeat the last event till it ends
        while last_time_event_happend <= G.simulation_length:
            time_index.append(last_time_event_happend)
            last_time_event_happend+=1
            events.append(event)
        
        #Create a DataFrame of queue events and number in system
        
        df = pd.DataFrame(events)
        df.columns = ["Number in System"]
        df.index = time_index
        fig = px.line(df, x=df.index, y="Number in System", title='Queue Path')
        
        if plot:
            fig.show()
        
        return df
       
    def queue_path_number_in_queue(self,plot=True):
        #TO DO
        #Do similar technique to keep track the number in queue
        
        #Create a time index to identify the time units passed in queue run
        #What it does it creates unit time indicies to record the times when nothing happened
        #and when times sth happened. E.g in 3.2 sbd came then it creates 0,1,2,3,3.2,4 
        #Time indicies
        time_index_queue = []
        index = 0
        
        #Events with the same logic. It should repeat the previous num in system till it updates
        events_queue = []
        event = 0
        
        for items in range(len(G.change_in_queue)):
            
            while index < G.change_in_queue[items]:
                time_index_queue.append(index)
                events_queue.append(event)
                index+=1
            event = G.num_in_queue[items]
            events_queue.append(event)
            time_index_queue.append(G.change_in_queue[items])
        
        #Also add the last events if nothing happens until the simulation ends
        last_time_event_happend = int(time_index_queue[-1]) + 1
        
        #Add the indicies and plus since nothing happend repeat the last event till it ends
        while last_time_event_happend <= G.simulation_length:
            time_index_queue.append(last_time_event_happend)
            last_time_event_happend+=1
            events_queue.append(event)
        
        #Create a DataFrame of queue events and number in system
        
        df_q = pd.DataFrame(events_queue)
        df_q.columns = ["Number in Queue"]
        df_q.index = time_index_queue
        fig = px.line(df_q, x=df_q.index, y="Number in Queue", title='Queue Path')
        
        if plot:
            fig.show()
        
        return df_q
        
    def queue_statistics(self):
        
        df_stats = pd.DataFrame([G.queue_time,G.serv_time,G.system_time]).T
        df_stats.columns = ["Queue Times","Service Times","System Times"]
        
    
        return df_stats
    
    #I think its correct
    def calc_idle_time(self):
        #Take the data
        data = self.queue_path_plot(plot=False).reset_index()
        diffs = data["index"].diff(periods = 1)
        
        idle_time = 0
        i = 0
        while i < len(data)-1:
            #If num in system is 0 add the difference to the idle time
            if data.iloc[i,1] == 0:
                idle_time+= diffs.iloc[i+1]
            i+=1
                
        return idle_time
    
    #Calculate statistics and Little's formulas
    def calc_stats(self):
        
        stats_df = self.queue_statistics()
        
        exp_Tq = stats_df["Queue Times"].sum() / len(stats_df["Queue Times"])

        exp_T = stats_df["System Times"].sum() / len(stats_df["System Times"])

        exp_S = stats_df["Service Times"].sum() / len(stats_df["Service Times"])   

        L = G.arrival_rate * exp_T

        L_q = G.arrival_rate*exp_Tq

        idle_time = self.calc_idle_time()
        busy_time = G.simulation_length - idle_time

        traff_intensity = 1 - idle_time / G. simulation_length
        
        return exp_T,exp_Tq,exp_S,idle_time,busy_time,traff_intensity
        



average_time_in_system = []
average_queue_wait = []
average_service_time = []
idle_times = []
busy_times = []
intensities = []
arrival_rates = []
service_rates = []
run_lengths = []
assumed_intensities = []
difference = []
for run in range(G.number_of_runs):
    
    #Run simulation
    sim_model = Simulation_Model()
    sim_model.run()
    
    #Record statistics
    exp_T,exp_Tq,exp_S,idle_time,busy_time,traff_intensity = sim_model.calc_stats()
    
    average_time_in_system.append(exp_T)
    average_queue_wait.append(exp_Tq)
    average_service_time.append(exp_S)
    idle_times.append(idle_time)
    busy_times.append(busy_time)
    intensities.append(traff_intensity)
    arrival_rates.append(1 / G.arrival_rate)
    service_rates.append(1 / G.service_rate)
    run_lengths.append(G.simulation_length)
    assumed_intensities.append( (1 / G.arrival_rate ) /  (1 / G.service_rate))
    difference.append((1 / G.arrival_rate ) /  (1 / G.service_rate) - traff_intensity)
    #Reset the statistics
    G.reset_stats()
    
    #Randomly change arrival and service rates within reasonable values 
    G.arrival_rate = 1.0 / np.random.randint(low= 1 , high = 5)
    G.service_rate = 1.0 / np.random.randint(low= 4 , high = 10)
    
    
    

stored_stats = pd.DataFrame([average_time_in_system,average_queue_wait,
                             average_service_time,idle_times,busy_times,intensities,
                             arrival_rates,service_rates,assumed_intensities,run_lengths,difference]).T
stored_stats.columns = ["Average Time in System","Average Wait Time in Queue","Average Service Time",
                        "Idle Time of Server","Busy Time of Server","Traffic Rate","Arrival Rate",
                        "Service Rate","Assumed Intensities","Run Lengths","Intensity Error Simulation vs Formula"]
    
    
stored_stats.to_excel("Simulation_Verification.xlsx")
    
#Go back to take another run