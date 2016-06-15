#!/bin/usr/python
import os

nfiles     = 5
folder_in  = "/data/uclhc/uci/user/amete/truth_analysis/inputs/sample_list"
folder_out = "/data/uclhc/uci/user/amete/truth_analysis/inputs/sample_list_split"

def file_len(f):
    for i, l in enumerate(f):
        pass
    return i + 1

def main():
    files = [ f for f in os.listdir(folder_in) if os.path.isfile(os.path.join(folder_in, f))]

    iteration=1
    for f in files:
        input_file  = open('%s/%s'%(folder_in,f))
        total_files = file_len(input_file) 
        input_file.seek(0)
        print '\nFile %s has %i lines'%(f, total_files)
        if total_files > nfiles:
            total_files_to_write = int(total_files/nfiles) + 1
            print '\t Total files to write %i'%(total_files_to_write)
            for ii in xrange(total_files_to_write):
                output_file_dsid = f.split('.')[1]
                output_file_name = f.replace('%s'%(output_file_dsid),'%s_%s'%(output_file_dsid,str(ii)))
                print '\t Writing file %s'%(output_file_name)
                output_file = open('%s/%s'%(folder_out,output_file_name),'w')
                for line in xrange(nfiles):
                    current_file = input_file.readline()
                    output_file.write('%s'%current_file)
                output_file.close()
        else:
            print 'File already has fewer lines...'
        input_file.close()

if __name__ == '__main__':
    main()
