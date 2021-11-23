
import re
import pickle


def main():
    filename = "raw_data/berlin_zip_codes.txt"

    zip_code_list = []
    with open(filename) as file:
        for line in file:
            found = re.search(r"\d{5}", line)
            if found:
                zip_code_list.append(found.group(0))
    
    with open('raw_data/zip.pkl', 'wb') as f:
        pickle.dump(zip_code_list, f)


    return zip_code_list


if __name__ == "__main__":
    print("saved the following zip codes to file:", main())

