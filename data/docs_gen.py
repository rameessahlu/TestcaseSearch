import json

test_cases = []
source_file = 'test_case_names.txt'
dest_file = 'test_cases.json'

def generate_test_cases():
    id_count = 0
    with open(source_file) as tcn:
        for line in tcn:
            tc = {}
            tc['_index'] = 'test_cases'
            tc['_type'] = 'test_case'
            tc['id'] = id_count
            tc['_source'] = {
                'id': id_count,
                'name': line[:-2],
                'designedBy': '',
                'description': '',
                'dependencies':'',
                'data': '',
                'exp_result': '',
                'priority': '',
                'steps': []
                }
            test_cases.append(tc.copy())
            id_count = id_count + 1

    output_file = open(dest_file, 'w', encoding='utf-8')
    json.dump(test_cases, output_file)
    #for tc in test_cases:
    #    json.dump(tc, output_file)
    #    output_file.write("\n")


if __name__ == '__main__':
    generate_test_cases()
