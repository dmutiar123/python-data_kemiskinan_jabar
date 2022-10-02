import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("bps_kemiskinanjabar.csv")
print("1. head \n" ,df.head())

# menhapus kolom yg tidak terpakai
df=df.drop(columns=["kode_provinsi","kode_kabupaten_kota","id"])

# mengganti kabupdaten menjadi kab agar lebih singkat
df["nama_kabupaten_kota"]=df["nama_kabupaten_kota"].str.replace("KABUPATEN","KAB")

# cek angka aneh
#fig,ax=subplot()
#ax.plot(df[])

#cek missing value
print("\n 02. cek missing value: \n \n",df.isna().sum())
#tidak ada missing value

#cek isi columns

print("\n 03. cek isi columns nama kabupaten : \n \n",df.value_counts(["nama_kabupaten_kota"]))
print("\n 04. cek isi columns tahun : \n \n",df.value_counts(["tahun"]))

#membuat index

df_indextahun=df.set_index(["tahun","nama_kabupaten_kota"])

# melihat 5 wilayah dengan kemiskinan tertinggi di setiap tahun
print("\n 05. Lima wilayah dengan tingkat kemiskinan tertinggi di setiap tahun")

list_tahun = [2018,2019,2020]

for thn in list_tahun:
    df_tahun=df[df["tahun"]==thn]
    df_tahun=df_tahun.groupby(["tahun","nama_kabupaten_kota"])["indeks_kedalaman_kemiskinan"].sum().sort_values(ascending=False).head(5)
    print("\n",df_tahun)


print(" \n 06. tingkat kemiskinan wilayah di tahun 2018-2020 ")

df_pivot= pd.pivot_table(data=df,index="nama_kabupaten_kota",columns="tahun")

print(df_pivot)

# mencari selisih tingkat kemiskinan wilayah

# indeks min kemiskinan wilayah
df_pivot2= pd.pivot_table(data=df,index="nama_kabupaten_kota",aggfunc={"indeks_kedalaman_kemiskinan":np.max})
# indeks max kemiskinan wilayah
df_pivot3= pd.pivot_table(data=df,index="nama_kabupaten_kota",aggfunc={"indeks_kedalaman_kemiskinan":np.min})
# selisih max-min indeks kemiskinan
df_sel=df_pivot2-df_pivot3
# sort indeks kemiskinan
df_sel=df_sel.head(5).sort_values(by="indeks_kedalaman_kemiskinan",ascending=False)
print("\n 5 wilayah dengan selisih indeks kemiskinan terbesar",df_sel)

# grafik selisih indeks kemiskinan

import matplotlib.pyplot as plt
import seaborn as sns

sns.barplot(data=df_sel,x=df_sel.index,y="indeks_kedalaman_kemiskinan")
plt.xticks(rotation=45)
plt.show()

#melihat indeks kemiskinan pertahun

df_pertahun=df.groupby("tahun")["indeks_kedalaman_kemiskinan"].sum()
print("\n indeks kemiskinan pertahun",df_pertahun)

sns.barplot(data=df,x="tahun",y="indeks_kedalaman_kemiskinan")
plt.show()

# membuat grafik 5 besar indeks kemiskinan di setiap tahun
fig, ax=plt.subplots(3)
ax[0].barplot(df["tahun"]==2018,df["indeks_kedalaman_kemiskinan"])
ax[1].barplot(df["tahun"]==2019,df["indeks_kedalaman_kemiskinan"])
ax[2].barplot(df["tahun"]==2020,df["indeks_kedalaman_kemiskinan"])
ax[1].set_xlabel("tahun")
plt.show()


