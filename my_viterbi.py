import sys

class Viterbi:
    def __init__ (self):
        self.q = {} #transition probability 
        self.e = {} #emission probability
        
        self.tags= ['phi','noun', 'verb', 'inf', 'prep', 'fin']

    
    def fileparser(self,fname):
        #-------------Parses file and creates dictionary for transition and emission probability-----------
        with open(fname) as fhandle:
            for line in fhandle:
                line_list = line.split()
        
                if line_list[0] in self.tags:
                    if line_list[0] in self.q:
                        self.q[line_list[0]][line_list[1]] = float(line_list[2])
                    else:
                        self.q[line_list[0]] = {}
                        self.q[line_list[0]][line_list[1]] = float(line_list[2])
                else:
                    if line_list[0] in self.e:
                        self.e[line_list[0]][line_list[1]] = float(line_list[2])
                    else:
                        self.e[line_list[0]] ={}
                        self.e[line_list[0]][line_list[1]] = float(line_list[2])
   
            
    def findSentenceSequence(self,word_list):
        #Input: word_list : sequence of word as sentence 
        #Output: tag sequence for the sentence
        
        num_of_words = len(word_list)
        backptr_viterbi_tag= [{}]*(num_of_words-1)
        viterbi_pi = [{}]*num_of_words
        forward_pi = [{}]*num_of_words
        
        for i in range(num_of_words):
            viterbi_pi[i] = {'noun':0, 'verb':0, 'inf':0, 'prep':0}
            forward_pi[i] = {'noun':0, 'verb':0, 'inf':0, 'prep':0}
            

        for word_index,word in enumerate(word_list):
            for tag in self.tags[1:len(self.tags)-1]:
                if word_index==0:
                    temp_q = self.q[tag]['phi'] if 'phi' in self.q[tag] else 0.0001
                    temp_e = self.e[word][tag] if word in self.e and tag in self.e[word] else 0.0001
                    viterbi_pi[word_index][tag] = temp_q * temp_e
                    forward_pi[word_index][tag] = temp_q * temp_e
                else:
                    for prev_tag in self.tags[1:len(self.tags)-1]:
                        temp_q = self.q[tag][prev_tag] if prev_tag in self.q[tag] else 0.0001
                        temp_e = self.e[word][tag] if word in self.e and tag in self.e[word] else 0.0001
                        temp_value = viterbi_pi[word_index-1][prev_tag] * temp_q * temp_e
                        
                        if temp_value > viterbi_pi[word_index][tag]:
                            temp_best_previous_tag = prev_tag
                            viterbi_pi[word_index][tag] = temp_value 
                        forward_pi[word_index][tag] += temp_value
                        
                    #updating final backptr network values 
                    backptr_viterbi_tag[word_index-1][tag] = temp_best_previous_tag
            
            
        #-----------Last result "Tag" calculcation---------------------------------------------------------------------
        result_best_pi_value =0 
        for tag in self.tags[1:len(self.tags)-1]:
            temp_q = self.q['fin'][tag] if tag in self.q['fin'] else 0.0001
            temp_pi_value = viterbi_pi[-1][tag]*temp_q
            result_best_pi_value = max(result_best_pi_value, temp_pi_value)
        
        
        #--------------------------Printing values ---------------------------------------------------------------------
        print("PROCESSING SENTENCE:" + str(word_list))
        print("")

        print("FINAL VITERBI NETWORK")
        for word_index,word in enumerate(word_list):
            for tag in self.tags[1:len(self.tags)-1]:
                print("P(" + word +"="+ tag +") = "+str(viterbi_pi[word_index][tag]))
                
        print("")        
        print("FINAL BACKPTR NETWORK")
        for word_index,word in enumerate(word_list[1:]):
            for tag in self.tags[1:len(self.tags)-1]:
                print("Backptr(" + word +"="+ tag+ ") = "+ str(backptr_viterbi_tag[word_index][tag]))
        
        
        print("")
        print("BEST TAG SEQUENCE HAS PROBABILITY =" + str(result_best_pi_value))
        for word_index in range(len(word_list)-1,-1,-1):
            word= word_list[word_index]
            temp_dict_values= list(viterbi_pi[word_index].values())
            temp_dict_keys  = list(viterbi_pi[word_index].keys())
            best_tag_for_word= temp_dict_keys[temp_dict_values.index(max(temp_dict_values))]
            print(word + "->" + best_tag_for_word)
        
        
        
        print("")
        print("")
        print("FORWARD ALGORITHM RESULTS")
        for word_index,word in enumerate(word_list):
            for tag in self.tags[1:len(self.tags)-1]:
                print("P(" + word +"="+ tag +") = "+str(forward_pi[word_index][tag]))
        
        print("------------------------------------------------------------------")
    

def main():
    args = sys.argv[1:]
    if len(args)>2 or len(args)<2:
        print "Input arguments insufficient"
    probability_file = args[0]
    sentence_file    = args[1]
    v= Viterbi()
    v.fileparser(probability_file)
    
    fname = open(sentence_file)
    for line in fname:
        line= line.lower()
        line= line.split()
        v.findSentenceSequence(line)


if __name__ == "__main__":
  main()