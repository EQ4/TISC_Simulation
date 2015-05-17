#!/usr/bin/env python

# Simulates the output of the GLITC 

from array import array
import numpy as np



def sum_correlate(num_samples,a_dig_waveform,b_dig_waveform,c_dig_waveform,threshold,TISC_sample_length=16,delay_type_flag=0,average_subtract_flag=0,correlation_mean=np.zeros(44),trial_run_number=1):
   import matplotlib.pyplot as plt
   #speed_of_light = 2.99*10**8
   #sample_period = 3.5810**(-10)
   #ab_distance = 1.0
   #ac_horz_distance = 1.17
   #ac_vert_distance = 4.7
   #ac_distance = np.sqrt((ac_horz_distance)**2+(ac_vert_distance)**2)

   trigger_flag = 0
   if (delay_type_flag == 1):
      GLITC_delays = np.array([[0,0,0],
                           #[0,-1,2],
                           #[0,-1,3],
                           #[0,-1,4],
                           #[0,-1,5],
                           #[0,-1,6],
                           #[0,-1,7],
                           [0,0,4],
                           [0,0,5],
                           [0,0,6],
                           [0,0,7],
                           [0,0,8],
                           [0,0,9],
                           [0,0,10],
                           [0,0,11],
                           [0,0,12],
                           [0,0,13],
                           [0,0,14],
                           [0,1,14],
                           [0,1,15],
                           [0,1,16],
                           [0,1,17],
                           [0,2,18],
                           [0,2,19],
                           [0,2,20],
                           [0,2,21],
                           [0,3,21],
                           [0,3,22],
                           [0,3,23],
                           [0,3,24],
                           [0,3,25],
                           [0,4,26],
                           [0,4,26],
                           [0,4,27],
                           [0,4,28],
                           [0,4,29],
                           [0,5,27],
                           [0,5,28],
                           [0,5,29],
                           [0,5,30],
                           [0,5,31],
                           [0,5,32],
                           [0,5,33],
                           [0,6,29],
                           [0,6,30],
                           [0,6,31],
                           [0,6,32],
                           [0,6,33],
                           [0,6,34],
                           [0,6,35]])
         
      #GLITC_delays = np.array([[0,0,0],[1,0,0]])
         
   
###############################################
# Do Sum correlation
###############################################
   
   #print correlation_mean
   prev_sum = np.zeros(len(GLITC_delays))
   this_sum = np.zeros(len(GLITC_delays))
   total_sum = np.zeros(len(GLITC_delays))
   temp_sum = np.zeros(len(GLITC_delays))
   max_total_sum = 0
   add_AB = [0] * TISC_sample_length
   add_ABC = [0] * TISC_sample_length

   best_chunk = 0
   b_lower_index_limit = 0
   c_lower_index_limit = 0
   trigger_flag = 0
   if (delay_type_flag == 1):
      square_sum_ABC = np.zeros(len(GLITC_delays))
      previous_square_sum = np.zeros(len(GLITC_delays))
   else:
      square_sum_ABC = np.zeros(200*num_samples)
      previous_square_sum = np.zeros(200*num_samples)
      delays = np.zeros((200*num_samples,3))
      i = 0

   # Use GLITC Firmware Delays
   if (delay_type_flag == 1):
      
      # Build two 16 sample sums
      for chunk in range(0,2):
         previous_square_sum = square_sum_ABC
         square_sum_ABC= np.zeros(len(GLITC_delays))

         # Get sum correlation for 16 samples
         for i in range(0,len(GLITC_delays)):
            # Determine the starting position for each sample
            a_start_pos = chunk*TISC_sample_length+GLITC_delays[i][0]
            b_start_pos = chunk*TISC_sample_length+GLITC_delays[i][1]
            c_start_pos = chunk*TISC_sample_length+GLITC_delays[i][2]
            
            # Add each sample at given delay
            add_AB = np.add(a_dig_waveform[a_start_pos:a_start_pos+TISC_sample_length],b_dig_waveform[b_start_pos:b_start_pos+TISC_sample_length])
            add_ABC = np.add(add_AB,c_dig_waveform[c_start_pos:c_start_pos+TISC_sample_length])
            square_ABC = add_ABC**2
            square_sum_ABC[i] = np.sum(square_ABC)

      # Add all the two sums for each delay
      total_sum = np.add(square_sum_ABC,previous_square_sum) 
      
      # Find the maximum sum
      max_total_sum = np.amax(total_sum)
      
      # Find the delays for the largest sum
      best_delays = GLITC_delays[np.argmax(total_sum)]
      
      if(average_subtract_flag):
         if (trial_run_number>0):
            correlation_mean = (1.0/trial_run_number)*(((trial_run_number-1)*correlation_mean)+total_sum)
         as_total_sum = np.subtract(total_sum,correlation_mean)
         as_max_total_sum = np.amax(as_total_sum)
         as_best_delays = GLITC_delays[np.argmax(as_total_sum)]
      #print trial_run_number
      #print correlation_mean[10]
      #print total_sum
      #print "\n"
      #print total_sum
      #print len(total_sum)
      #print len(GLITC_delays)
      #print "Max Sum: "+str(max_total_sum)
      #print best_delays

   else:

      #Set the lower index limit of Ch B/C
      for chunk in range(0,(num_samples/TISC_sample_length)):
         b_lower_index_limit = 0
         c_lower_index_limit = 0
         previous_sum_ABC = square_sum_ABC

         # Shift Ch B/C around
         for b in range(b_lower_index_limit,len(a_dig_waveform)-TISC_sample_length):
            for c in range(c_lower_index_limit,len(a_dig_waveform)-TISC_sample_length):
               this_sum = 0
               add_AB = np.add(a_dig_waveform[chunk*TISC_sample_length:(chunk*TISC_sample_length)+TISC_sample_length],b_dig_waveform[b:TISC_sample_length+b])
               add_ABC = np.add(add_AB,c_dig_waveform[c:TISC_sample_length+c])
               square_ABC = add_ABC**2
               square_sum_ABC[i] = np.sum(square_ABC)
               delays[i] = [chunk*TISC_sample_length,b,c]
               i += 1
               #print "a: "+str(chunk*TISC_sample_length)+":"+str((chunk*TISC_sample_length)+TISC_sample_length)+"\tb: "+str(b)+":"+str(b+TISC_sample_length)+"\tc: "+str(c)+":"+str(c+TISC_sample_length)
                  
      total_sum = np.add(square_sum_ABC,previous_square_sum)
      max_total_sum = np.amax(total_sum)
      best_delays = delays[np.argmax(total_sum)]
      
      #print total_sum
      #print "Max sum: " +str(max_total_sum)
      #print best_delays

   if(max_total_sum > threshold):
      trigger_flag = 1
      #print "Event passes"
      
  #print "Threshold: " + str(threshold)
   #print "max_total_sum: " + str(max_total_sum)
   #print "A Chunk: " + str(best_chunk)
   #print "B Delay: " + str(best_b_delay)#+'\t'+str(b_input_delay-best_b_delay)
   #print "C Delay: " + str(best_c_delay)#+'\t'+str(c_input_delay-best_c_delay)
   #print "\n\n"
   
   if (average_subtract_flag):
      return trigger_flag, max_total_sum, as_max_total_sum, correlation_mean
   else:
      return trigger_flag, max_total_sum


if __name__ == '__main__':
   import numpy as np
   from impulse import impulse_gen
   from digitizer import digitize
   import matplotlib.pyplot as plt
   from noise import generate_noise
   threshold = 300
   num_samples = 74
   upsample = 10
   num_bits = 3
   noise_mean = 0
   noise_rms = 20
   SNR = 2
   num_upsamples = num_samples*upsample
   a_dig_waveform = np.zeros(num_upsamples)
   a_waveform = np.zeros(num_samples)
   #a_dig_waveform[20] = 3.5
   #a_dig_waveform[21] = -3.5
   #a_dig_waveform[22] = 2.5
   #a_dig_waveform[23] = -2.5
   a_delay = 20
   b_delay = 10
   c_delay = 10
   TISC_sample_length = 16
   delay_type_flag = 1
   average_subtract_flag = 1
   #global correlation_mean
   correlation_mean = np.zeros(44)
   correlation_mean.fill(50)
   filter_flag = 0
   
   signal_amp = SNR*2*noise_rms

   for i in range(0,10):
      a_waveform = impulse_gen(num_samples,a_delay,upsample,draw_flag=0,output_dir='output/')
      a_waveform = np.add(a_waveform,generate_noise(num_samples,noise_mean,noise_mean,filter_flag))
      
      difference=np.amax(a_waveform)-np.amin(a_waveform) # Get peak to peak voltage
      a_waveform *= (1/difference) # Normalize input
      a_waveform *= signal_amp # Amplify
      
      a_dig_waveform = digitize(a_waveform,num_samples,upsample,num_bits,noise_mean,noise_rms,digitization_factor=0.5)
   
   

      #print num_samples
      #print a_dig_waveform
   
      print i
      passed_flag, max_sum, as_max_sum, correlation_mean = sum_correlate(num_samples,a_dig_waveform,np.roll(a_dig_waveform,b_delay),np.roll(a_dig_waveform,c_delay),
                                                threshold,TISC_sample_length=TISC_sample_length,delay_type_flag=delay_type_flag,
                                                average_subtract_flag=average_subtract_flag, correlation_mean=correlation_mean,run_number=i+1)
   print passed_flag
