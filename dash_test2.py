import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
plt.rc('font', family='AppleGothic') # 맥 컴퓨터

st.title('생산 귀책')

#---------Data Load-------------#
df_total = pd.read_excel('./Test_data.xlsx')
#-------------------------------#

## Human Error
st.header('Human Error')
defect_list = ['각도불량', '간극', '간섭','누락','사양불량','손상','발청','오염','외관불량','유격','이완','이종품','타각불량','혼입']
df_total = df_total.iloc[:,1:]
df_bad = df_total[(df_total['불량명'] == '누락') | (df_total['불량명'] == '이완') | (df_total['불량명'] == '이종품')]
df_cause = df_total[(df_total['원인명'] == '미조임') | (df_total['원인명'] == '미조립') | (df_total['원인명'] == '과조임') | (df_total['원인명'] == '조립불량') | (df_total['원인명'] == '제작불량')]
df_sum = pd.concat([df_cause, df_bad], axis=0, join='inner')
df_common = pd.merge(df_cause, df_bad)
df_factory = df_sum[(df_sum['귀책'] == '생산')]

# fig, ax = plt.subplots(figsize=(20,5))
# sns.countplot(x='월', data=df_factory, hue='귀책부서명')
# plt.xticks(rotation=-30)
# plt.title('월 별 귀책부서 Human Error')
# plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
# st.pyplot(fig)

pvt= df_factory[['귀책부서명', '월']].pivot_table(index='월', columns='귀책부서명', aggfunc=len)
# pvt = pvt.fillna(0)
st.bar_chart(pvt.to_dict())

st.write("생산 귀책 부서에 대한 Human Error 건수를 집계하였으며 4월부터 조립 2직의 Human Error 가 지속 Worst 사항임")

fig, ax = plt.subplots(figsize=(15,5))
cause_count = df_factory['원인명'].value_counts()
g = sns.countplot(x='원인명', data=df_factory, order = cause_count.index)
for i in range(cause_count.shape[0]):
    g.text(x=i, y=cause_count[i], s=cause_count[i], horizontalalignment='center')
plt.xticks(rotation=-30)
plt.title('Human Error 원인')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(10,5))
bad_count = df_factory['불량명'].value_counts()
g = sns.countplot(x='불량명', data=df_factory, order = bad_count.index)
for i in range(bad_count.shape[0]):
    g.text(x=i, y=bad_count[i], s=bad_count[i], horizontalalignment='center')
plt.xticks(rotation=-90)
plt.title('Human Error 불량')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15,5))
plt.figure(figsize=(10, 5))
sns.countplot(x='라인', data=df_factory, order=df_factory['라인'].value_counts().index)
plt.xticks(rotation=-45)
plt.title('라인별 Error')
st.pyplot(fig)

fig, ax = plt.subplots(figsize=(15,5))
df_worst = df_factory[(df_factory['불량명'] == '누락') | (df_factory['원인명'] == '조립불량')]
worst_count = df_factory['귀책부서명'].value_counts()
g = sns.countplot(x='귀책부서명', data=df_factory, order = worst_count.index)
for i in range(worst_count.shape[0]):
    g.text(x=i, y=worst_count[i], s=worst_count[i], horizontalalignment='center')
plt.xticks(rotation=-90)
plt.title('Worst 귀책')
st.pyplot(fig)


