import streamlit as st
import pandas as pd
from io import StringIO
import sys
import math
import yagmail
import os

def euclidian_dist(row, ideal_best,ncol):
    dist = 0
    for i in range(ncol):
        dist = dist+(row[i]-ideal_best[i])**2
    return math.sqrt(dist)

def main():
    st.title("Topsis Solver")
    st.markdown("**Instructions to be followed :**\n 1. File types allowed -> csv files only. \n 2. Number of weights and number of impacts must be same.Both must be equal to the number of features.")
    st.markdown("**Output will be sent via email as a csv file.**")
    with st.form(key='form1'):
        uploaded_file = st.file_uploader("Choose a file")
        weights = st.text_input(
        "Enter the weights 👇",
        )
        impacts= st.text_input(
        "Enter the impacts 👇",
        )
        email = st.text_input(
        "Enter the email 👇",
        )
        col1,col2,col3,col4,col5=st.columns(5)
        with col1:
            pass
        with col2:
            pass
        with col3:
            submit_button=st.form_submit_button(label="Submit")
        with col4:
            pass
        with col5:
            pass
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file,encoding='latin-1')
        nrow = data.shape[0]
        final = data.iloc[:, 1:]
        ncol = final.shape[1]
        for i in final.columns:#col
            sum = 0
            for j in range(nrow): 
                sum = sum+final.loc[j, i]**2
            final[i] = round(final[i]/math.sqrt(sum), 4)
        w1 = weights
        w = []
        for i in w1.split(','):
            w.append(int(i))
        j = 0
        for i in final.columns:
            final[i] = round(final[i]*w[j], 4)
            j += 1
        impact_st = impacts
        impact = []
        for i in impact_st.split(','):
            impact.append(i)
        ideal_best = []
        ideal_worst = []
        dist_ideal_best=[]
        dist_ideal_worst=[]
        j = 0
        for i in final.columns:
            if (impact[j] == "+"):
                ideal_best.append(final[i].max())
                ideal_worst.append(final[i].min())
            else:
                ideal_best.append(final[i].min())
                ideal_worst.append(final[i].max())
            j+=1
        j = 0
        for i in range(final.shape[0]):
            dist_from_ideal_best = euclidian_dist(final.iloc[i,:], ideal_best,ncol)
            dist_from_ideal_worst = euclidian_dist(final.iloc[i,:], ideal_worst,ncol)
            dist_ideal_best.append(dist_from_ideal_best)
            dist_ideal_worst.append(dist_from_ideal_worst)
        final['S+'] = dist_ideal_best
        final['S-'] = dist_ideal_worst
        performance_score = []
        for i in range(nrow):
            p_score = (dist_ideal_worst[i])/(dist_ideal_best[i]+dist_ideal_worst[i])
            performance_score.append(round(p_score, 4))
        data['Topsis score'] = performance_score
        data['Rank'] = (data['Topsis score'].rank(method='max', ascending=False))
        data = data.astype({'Rank': int})
        data.to_csv('output.csv', index=False)
        if submit_button:
            try:
                yag = yagmail.SMTP('akshatgirdhar02@gmail.com', 'ocyuxqgobnrtelri')
                yag.send(to = email,
                subject = 'Output File for Topsis',
                contents = "Please find the attachment below",
                attachments=['output.csv'])
                st.write("Email sent")
            except:
                st.write("Email not sent ")

if __name__=="__main__":
    main()