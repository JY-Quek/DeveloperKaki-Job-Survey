
import collections
from wordcloud import WordCloud
    

def freq_counter(df):
    person_tech_used = df.tech_used.to_list()
    tech_involved = []
    for tech_input in person_tech_used:
        tech_input_list = [x.lower().strip() for x in tech_input.split(",")]   
        tech_involved += tech_input_list
        
    occurrences = collections.Counter(tech_involved)
    wordcloud_img = WordCloud(width = 1200, height = 800).generate(" ".join(tech_involved))
    return occurrences, wordcloud_img


def calculate_density(target_tech_list, df):
    person_tech_used = df.tech_used.to_list()
    density_tech_person = {}
    
    for tech_input in person_tech_used:
        tech_input_list = [x.lower().strip() for x in tech_input.split(",")]
        for target_tech in target_tech_list:
            if target_tech in tech_input_list:
                density_tech = 1/len(tech_input_list) # Calculate the density of tech in each person
            
                if target_tech not in density_tech_person:
                    density_tech_person[target_tech] = [ density_tech ]
                else:
                    density_tech_person[target_tech].append(density_tech)
        
    # Find the average value of density from every person
    output_density = {}
    for target_tech in density_tech_person:
        lst = density_tech_person[target_tech]
        output_density[target_tech] = sum(lst) / len(lst)
    
    # Sort the dictionary
    output_density = dict(sorted(output_density.items(), key=lambda item: item[1], reverse=True))
    return output_density                