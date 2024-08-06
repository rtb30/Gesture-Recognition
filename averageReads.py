# import
import pandas as pd

def averageReads(data_new, EPC_count, labels, saveMe, EPC_sep):
    count = 0
    sum = 0
    cols = []
    data_len = len(data_new)

    sum_dict = {i: 0 for i in range(1, EPC_count + 1)}
    count_dict = {i: 0 for i in range(1, EPC_count + 1)}
    label_dict = {i: 0 for i in range(1, 21)}

    for i in range(1, 22):
        label_dict[i] = (f'gesture{i}')

    cols.append('EPC')
    for i in range(1, 22):
        cols.append(f'gesture{i}')

    df = pd.DataFrame(columns = cols)

    for i in range(EPC_count):
        df.loc[i, 'EPC'] = f'A{i+1}'

    for j in range(1, EPC_count + 1):
        print(f'Finding A{j} tags')
        for i in range(len(data_new)):
            sum = sum + data_new[i]['EPC'].value_counts().get(j, 0)
    
            count = count + 1
    
            if(count == 15):
                df.loc[j-1, labels[i]] = sum
                print(f'{labels[i]} has a total of {sum} tags')

                count = 0
                sum = 0

        k = 0
        print()


    '''
    for EPC_df in EPC_sep:
        if not EPC_df.empty:
            EPC_value = EPC_df['EPC'].iloc[0]
            #print(f'Finding A{EPC_value} tags')
            sum_dict[EPC_value] += EPC_df['EPC'].value_counts().get(EPC_value, 0)
            count_dict[EPC_value] += 1

    print(sum_dict)

    for i in range(data_len):
        for j in range(1, EPC_count + 1):
            df.loc[j-1, labels[i]] = sum_dict[j]
    '''

    df.to_csv(saveMe, index = False)