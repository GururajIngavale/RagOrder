import pandas as pd
import numpy as np
import mplfinance as plt
import json



def find_fvg_levels(dfl,strd):
    """
    Detects all BISI and SISI FVGs in given OHLC DataFrame.
    df must have columns: ['open', 'high', 'low', 'close']
    Returns a list of tuples: (type, low_level, high_level)
    where type is 'BISI' or 'SISI'
    """
    fvg_list = []

    
        
# whole days or date ranges
    # b=dfl['2024-06-01':'2024-06-02']            # inclusive of end
    a= dfl.loc[strd:] if not(pd.isna(strd)) else dfl
    df = a.reset_index(drop=True)# index 0,1,2.....
    print(df)

    for i in range(len(df) - 2):
        c1, c2, c3 = df.loc[i], df.loc[i+1], df.loc[i+2]
        h1=c1['high']
        l1=c1['low']
        
        l3=c3['low']
        h3=c3["high"]

        # BISI condition (Buy-side imbalance)
        if h1 < l3:
            # low = entry['low']
            # high = entry['high']
            formation_last_index = i+3 #entry['i3']  # FVG formed at i1,i2,i3 -> only check candles after i3

            # Now scan subsequent candles for any touch
            valid = True
            touch_idx = None
            for j in range(formation_last_index , len(df)):
                c = df.loc[j]
                # print(valid)
                # if candle intersects zone at all -> touched
                if (c['low'] <= l3 ) :
                    valid = False
                    touch_idx = j

                    break
                

            if valid:
                fvg_list.append(('BISI', c1['high'], c3['low']))
            #     # determine mask for whole zone and reset all of it in fzone
            #     mask = (fzone.index >= low - 1e-9) & (fzone.index <= high + 1e-9)
            #     fzone.loc[mask, tf] = False

            #     # remove numeric mapping(s) in ftap: set any cell within mask to 0
            #     ftap.loc[mask, tf] = 0

            #     # update metadata
            #     entry['mitigated'] = True
            #     entry['mitigation_index'] = touch_idx

            
        # SISI condition (Sell-side imbalance)
        elif l1 > h3:
        
            
            formation_last_index = i+3

            # Now scan subsequent candles for any touch
            valid = True
            touch_idx = None
            for j in range(formation_last_index , len(df)):
                c = df.loc[j]
                print(c)
                print(valid)
                print(j)
                print(i)
                # if candle intersects zone at all -> touched
                if (c['high'] >= h3 ) :
                    print("hi")
                    valid = False
                    touch_idx = j
                    break
                

            if valid:
                print("goog")
                fvg_list.append(('SISI', c3['high'], c1['low']))
    
    
    return fvg_list


# def build_fvg_matrix(price_range, timeframe_dfs):
    """
    Builds a DataFrame (rows=price levels, cols=timeframes)
    with True/False where FVG exists at that price for that timeframe.

    price_range : list or np.array of prices to mark (ex: range(90,130))
    timeframe_dfs : dict like {'5m': df_5m, '15m': df_15m, '1h': df_1h}
    """
    # Initialize all as False
    fvg_matrix = pd.DataFrame(False, index=price_range, columns=timeframe_dfs.keys())

    for tf, df in timeframe_dfs.items():
        fvg_zones = find_fvg_levels(df)

        for fvg_type, low, high in fvg_zones:
            # mark all prices between low and high as True (FVG exists)
            mask = (fvg_matrix.index >= low) & (fvg_matrix.index <= high)
            fvg_matrix.loc[mask, tf] = True

    return fvg_matrix

def fvgtap(ftapmat=pd.DataFrame(),fzonemat=pd.DataFrame(),data=pd.DataFrame(),ltime=pd.Timestamp()):
    # fdicti={"15m":data.resample('15T').ohlc(),
    forfvg={}
   
    forfvg[5]  = data
    if len(data)%3==0:
        forfvg[35]  = data.resample("15T").ohlc()
        if len(data)%9==0:
            forfvg[125]= data.resample("45T").ohlc()
        if len(data)%6==0:
            forfvg[80]= data.resample("30T").ohlc()
            if len(data)%12==0:
                forfvg[170]= data.resample("H").ohlc()
                if len(data)%24==0:
                    forfvg[350]=data.resample("2H").ohlc()
                    if len(data)%48==0:
                        forfvg[710]=data.resample("4H").ohlc()

                if len(data)%36==0:
                    forfvg[530]= data.resample("3H").ohlc()

    # Step 1: Pre-calculate all frequencies (avoid repeated pd.infer_freq)
    tf_freqs = {tf: pd.infer_freq(df) for tf, df in forfvg.items()}
    # Step 2: Pre-calculate column positions (for direct .iloc access)
    col_positions = {col: i for i, col in enumerate(ftapmat.columns)}

    # Step 3: Get base price and scale factor for position calculation
    base_price = 2000.00
    scale = 100

    # Step 4: Collect all updates in memory (avoid repeated .loc assignments)
    updates_by_index = {}

    for tf, df in forfvg.items():
        fvg_zones = fvg_zones(df, ltime-pd.Timedelta(minutes=tf))
        ij = tf_freqs[tf]  # ✅ yaha se milga hame column name in string by that special number
        
        for type, low, high in fvg_zones:
            # Decide target index and value
            target_idx = high if type == 'BISI' else low
            target_val = low if type == 'BISI' else high
            
            # Store in memory dictionary
            if target_idx not in updates_by_index:
                updates_by_index[target_idx] = {}
            
            updates_by_index[target_idx][ij] = target_val

    # Step 5: Batch apply all updates (optimized disc I/O)
    # Convert updates_by_index to structured arrays
    

    ftapmat_arr = ftapmat.values.copy()
    fzonemat_arr = fzonemat.values.copy()

    # Prepare data for vectorized operations
    updates_list = []
    for idx, col_dict in updates_by_index.items():
        row_pos = int((idx - base_price) * scale)
        for col, val in col_dict.items():
            g = int((val - base_price) * scale)
            col_pos = col_positions[col]
            updates_list.append((row_pos, col_pos, val, g))

    # Convert to NumPy array for vectorization
    if updates_list:
        updates_arr = np.array(updates_list, dtype=[('row', 'i4'), ('col', 'i4'), ('val', 'f8'), ('end', 'i4')])
        
        # Vectorized ftapmat update
        valid_mask = (updates_arr['row'] >= 0) & (updates_arr['row'] < len(ftapmat_arr))
        ftapmat_arr[updates_arr['row'][valid_mask], updates_arr['col'][valid_mask]] = updates_arr['val'][valid_mask]
        
        # Vectorized fzonemat update
        for row, col, val, g in updates_arr[valid_mask]:
            min_pos = min(row, g)
            max_pos = max(row, g)
            if 0 <= min_pos < len(fzonemat_arr):
                fzonemat_arr[min_pos:min(max_pos+1, len(fzonemat_arr)), col] = True

    # Write back
    ftapmat.iloc[:] = ftapmat_arr
    fzonemat.iloc[:] = fzonemat_arr
    return ftapmat,fzonemat

def run(data=pd.DataFrame(0,index=[0,1],columns=["high","low"]),lol=True):
    fzone=pd.read_parquet("ftap")
    ftap=pd.read_parquet("fzone")
    
    with open("fvglastcheckdate","r") as f:
            strd=pd.to_datetime(f.read())
        


    mask = (ftap.to_numpy() > 0).any(axis=1)#ye df ko 2d array me daal dega 
    forchek=ftap[mask]# yee sirf valued wali row dega
    if not(forchek.empty):
        id=forchek.index#ye upar wali kaa index
        for il in data.loc[strd+pd.Timedelta(minutes=1):].itertuples():# strd ka matlab hia ekk time jaha last time check kiya tha
            high=il.high
            low=il.low
            
            checked=forchek[(id<high) & (id>low)].dropna()#isme ab vo index hoo jayeygi joo mitigated ho chuki or reset hone wali hai 
            ftap.loc[checked.index,:]=0#reset ftap
            for m,end_val in checked.items():  # m=index, end_val=value
                fzone.loc[min(m, end_val):max(m, end_val), :] = False

    ftap,fzone=fvgtap(ftap,fzone,data,strd)

    ftap.to_parquet("ftap")
    fzone.to_parquet("fzone")
    with open("fvglastcheckdate","w") as f:
        f.write(data.index[-1])


    return ftap,fzone