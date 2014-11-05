import re
import os
import sys

# For people, like me, who are unaware of better ways to do this.

# Input CSV 'raw' file from sead plug
# Outputs CSV files, grouping sensor readings into respective files

# Must be in same folder as data

def chunk_data( file ):
   #sensor_id,data,microstamp,device_microstamp

   pattern = re.compile(r'([0-9]{2}),{1}(-?[0-9]*?.?[0-9]+?),{1}([0-9]+?),{1}([0-9]+)')

   chunks = re.findall(pattern, file)
   
   return chunks

def sort_data( chunks ):

   sid_record = set()
   data_lists = []
   
   # sid_record holds the different sids
   for line in chunks:
      if line[0] not in sid_record:
         sid_record.add(line[0])
         
   # adds data into data_lists
   # 2d list, grouping the respective sids' data
   for idx, sid in enumerate(sid_record):
      data_lists.append([])
      for line in chunks:
         if sid == line[0]:
            data_lists[idx].append(line)
   
   return data_lists

def export_lists( data_lists ):

   for idx_0, list in enumerate( data_lists ):
      
      file_name = "./sorted/{0}.csv".format( data_lists[idx_0][0][0] )
      dir = os.path.dirname( file_name )
      if not os.path.exists( dir ):
         os.makedirs( dir )
      f = open( file_name, "w" )
      
      for idx_1, line in enumerate(list):
         
         f.write( "{0},{1},{2},{3}\n".format( data_lists[idx_0][idx_1][0], data_lists[idx_0][idx_1][1], data_lists[idx_0][idx_1][2], data_lists[idx_0][idx_1][3] ) )
         
      f.close()

if __name__ == '__main__':

   if len(sys.argv) > 1:
      data_file = sys.argv[1]
   else:
      data_file = raw_input("Please enter name of data file --> ")
      
   chunks = chunk_data( open( data_file ).read() )
   
   data_lists = sort_data( chunks )
   
   export_lists( data_lists )
   