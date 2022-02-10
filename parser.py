import json
import requests
from bs4 import BeautifulSoup as bs

#hm_page = requests.get("http://www.thegoodscentscompany.com/categories.html")
#hm_soup = bs(hm_page.text, "html.parser")
#categories = {ele.text: ele.attrs['href'] for ele in hm_soup.select("a.buttonstyle")}
#print(categories)

categories = {"All Ingredients": "http://www.thegoodscentscompany.com/allprod-a.html"}

for cat in categories:
    print('* category: ', cat)
    cat_page = requests.get(categories[cat])
    cat_soup = bs(cat_page.text, "html.parser")
    alphabets = {ele.text: ele.attrs['href'] for ele in cat_soup.select(".alphaENIC1 span a")}

    #A,B,C,D, ...
    for alpha in alphabets:
        if alpha in "ABEFGHIJKLMNOPQRSTUVWXYZ":
            continue
        print('* alphabet: ', alpha)
        file_path = "./{}.json".format(alpha)
        data = {}
        alpha_page = requests.get(alphabets[alpha])
        alpha_soup = bs(alpha_page.text, "html.parser")
        
        alpha_soup = alpha_soup.select("td")
        items = {item.find("a").get_text(): str(item.find("a").attrs['onclick']).split("'")[1] \
               for item in alpha_soup if item.find("a") is not None}

        #ambrette seed, ...
        for item in items:
            print('* name: ', item)
            item_page = requests.get(items[item])
            item_soup = bs(item_page.text, "html.parser")

            cas_number = [ele.select_one(".radw11").get_text() for ele in item_soup.select(".cheminfo") if "CAS Number" in str(ele)]
            odor_type = [ele.get_text().split(": ")[-1] for ele in item_soup.select(".qinfr2") if "Odor Type" in ele.get_text()]
            odor_dscp = [ele.select("a") for ele in item_soup.select(".cheminfo") if "Odor Type" in str(ele)]
            pages = [ele.attrs['href'] for ele in item_soup.select("a") if 'Fragrance Demo Formulas' in ele.get_text()]

            #Demo Formula
            if len(pages) > 0:
                #print('* name: ', item) 
                #print("* CAS: ", cas_number)
                #print("* odor type: ", odor_type)
                if len(odor_dscp) > 0:
                    odor_dscp = [ele.get_text() for ele in odor_dscp[0]]
                #print("* odor dscp: ", odor_dscp)
                data[item] = {}
                data[item]["CAS"] = cas_number
                data[item]["type"] = odor_type
                data[item]["description"] = odor_dscp
                data[item]["demo"] = []

                demo_page = requests.get(pages[0])
                demo_soup = bs(demo_page.text, "html.parser")
                demos = demo_soup.select("td")
                for demo in demos:
                    class_name = str(demo).split("class")[1].split('"')[1]
                    if class_name == 'dmow1':
                        demo_name = demo.get_text()
                        data[item]["demo"].append({'name': demo_name, 'formula': {}})
                    elif class_name == 'dmow5':
                        odor_amount = demo.get_text()
                    elif class_name == 'dmow6':
                        odor_name = demo.string
                        if odor_name == 'Total':
                            data[item]["demo"][-1]['total'] = odor_amount
                        else:
                            data[item]["demo"][-1]['formula'][odor_name] = odor_amount
                #for ele in data[item]["demo"]:
                #    for key in ele:
                #        print("*", key, ": ",  ele[key])
                #print('='*20)
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)
                
                

