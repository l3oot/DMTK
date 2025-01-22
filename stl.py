import streamlit as st
import pandas as pd
import gspread
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import numpy as np

key = {
    "type": "service_account",
    "project_id": "genuine-ember-403902",
    "private_key_id": "9caa1a0008f5a0965818366654cbca20e79800dc",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDwlqbNPUlddfYV\nlxTbGZf6Vn9HSWoGJVfKeZSz9jH9ajPwPv9cYQWP2ti+bMsprSoka006SxPMyrTj\nU078JfAotKBBebhhCkVh7pn1f42PQS+5UUy90kGaEEC5/SMpbDV2muoNF3VWqzhu\nh1qCcq/8M2SE1znz1wOQFaynx00ZyjVF4WWIXUxpOHIbB2CprMMVZDZZfDT0R1Go\n27YENnxjibWOjqq+YfPNzk43eoQ4RBI2W8sB/EyqF/tJXiQ1sayTpB1/zRrjBLCw\ndiK7u5+zhJfTT0kQsklsWj52dMo713u2hS+W0poUYx5CbFjx9V40NRup/3GvEUNb\nJ2Hkcg5hAgMBAAECggEAC7fKuARcJmkwayzIn0NH27GK0XYJ6/K1q+7wBzPei3E4\nxmLLHTy8gJ0wIVY7LvR4MP3o7QXrGPZmiQvttOpEIDdr9sRu7osJhhOQ/BwSUP/j\nyyriifxLpa1U+boSlFno4LX64FhcJrSAMyH0jpX3bFk0dCPndrDqQ4JKvoE+iBrx\nAGL3b8w5W1GROTWrrRRVMemjSLWOsZJ9zKe4Z5tdTUkuwiJnonFk+vwDukpYnxdv\nxHyWq39yrfXCqx3dmGPLrJhbnNHsWLc0K5xZImKTbbIiJcPkPwvgwj0bCwC56dWg\nhtaWZbzBrhED5CN6sj94hm7/nEK+cubOxPS8AvFqAQKBgQD5TvFy3qU/g5Hr9ZBe\n+g+z48rDeqz8CODYtAMxxwdkStedc/JZ/hpeK3luIsBjlYIH7oGb4Gpu3ZmEgLL4\ndawuHeLXljmwov3KUhCH906x4baYe929r94ACEKaeGoY3hCItI4aAWTSyrUbvj0U\nUBjAjOcZKWtce9J2zOfXQrpNaQKBgQD3C8q/wSopzlF3zu/gvl6kL8SpN+zItWkW\n3AWqJcivdn3MxS8Z03H6A8aK4jHft+0ef1KNcKNV/JQ6ZxocfdMfeKO+HmKPQGJB\n5HNW294G0gAOG0o+yq8W2vXahR4wMtOXirKnhccCFsbgGRZWx4ro46dZf79+nLA6\nnBUeOfwCOQKBgB0eyncXaIflr1q3YTimzsS9W8a/gosh4lmNlT3wOH3PfCXpECrQ\n0nWjcFib+IrpQLn6cuspKGVwvujKO51n6Uett/xkkLKAJ1LFiSbIjUmbyr8+4KSy\ncSTh0h3G6OWkspu1M0/4T7WLdeIas3m27V04WBoJS4AO+oNj5cSwB6DZAoGBAKE7\nXPORCgeG07yxnfS7yeC2HE+kZDEJ1LBKoJfPWQ7K8od2GattSHG3jRiPT6WG0Iaa\n6jHNVYyE7+i96Vi29dcQUS1/fyunBXmjs3L4xAsHe2m5fddFSMhN1y7qui0Svu2k\nY7zZnmxKmTkgpme0i4A7M7lBmqTzdkCKJW44wbRhAoGBAJZcKnxjBHo3dBwauByN\nYc2iJuvNlc0PN6Jn2urPQcm1qh4eP+CjDtTgJVpB1UBLb/duSxcuVQC8pchdCXRt\n4sP5VFbsVW0Gq1fUQ37jbstso3XmGJfS8Cr8wiyVpwfA+H966bbJ5v8hS59yVniS\nKvgqUpUoCD266W8MnX4Z0eac\n-----END PRIVATE KEY-----\n",
    "client_email": "rpa-643@genuine-ember-403902.iam.gserviceaccount.com",
    "client_id": "101215475468738013271",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/rpa-643%40genuine-ember-403902.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com",
}
rcParams["font.family"] = "Tahoma"
# Configure Streamlit page
matplotlib.rcParams['font.family'] = 'TH Sarabun New'

st.set_page_config(page_title="ระบบวิเคราะห์ข้อมูลการนัดหมาย", layout="wide")


# Function to add value labels on bars
def add_value_labels(ax, spacing=5):
    for rect in ax.patches:
        y_value = rect.get_height()
        x_value = rect.get_x() + rect.get_width() / 2

        label = "{:,.0f}".format(y_value)

        ax.annotate(
            label,
            (x_value, y_value),
            xytext=(0, spacing),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=10,
        )


# Function to load data
@st.cache_data
def load_data():
    try:
        gc = gspread.service_account_from_dict(key)
        sheet = gc.open_by_key("1GxHdrdHrhFiDIz3Ac3YJvw7upr9GLpFzHMhHX64G4NU")
        df_username = sheet.worksheet("USERNAMES")

        df_username = pd.DataFrame(df_username.get_all_records())
        df_username = df_username.dropna(subset=["เบอร์"])
        df_username = df_username[df_username["เบอร์"].str.strip() != ""]

        return df_username
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {str(e)}")
        return None


# Add title
st.title("📊 ระบบวิเคราะห์ข้อมูลการนัดหมาย")

# Load the data
df_username = load_data()

if df_username is not None:
    tab1, tab2, tab3 = st.tabs(
        ["สถานะการนัดหมาย", "การนัดหมายตามประเภทแพทย์", "การนัดหมายตามวัน"]
    )

    with tab1:
        st.header("สถานะการนัดหมาย")

        total_count = len(df_username)
        confirmed_count = df_username[
            df_username["ผลการนัดหมาย"] == "ยืนยันการจองนัดหมาย"
        ].shape[0]
        wait_count = df_username[
            df_username["ผลการนัดหมาย"] == "รอเจ้าหน้าที่ดำเนินการ"
        ].shape[0]
        nconfirmed_count = df_username[
            df_username["ผลการนัดหมาย"] == "ไม่สามารถจองนัดหมายได้"
        ].shape[0]

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("ลงทะเบียนรวม", f"{total_count:,}")
        with col2:
            st.metric("ยืนยันการจอง", f"{confirmed_count:,}")
        with col3:
            st.metric("รอดำเนินการ", f"{wait_count:,}")
        with col4:
            st.metric("ไม่สามารถจอง", f"{nconfirmed_count:,}")

        # Create bar chart
        fig, ax = plt.subplots(figsize=(7, 3))
        data = {
            "หมวดหมู่": [
                "ลงทะเบียนรวม",
                "ยืนยันการจองนัดหมาย",
                "รอเจ้าหน้าที่ดำเนินการ",
                "ไม่สามารถจองนัดหมายได้",
            ],
            "จำนวน": [total_count, confirmed_count, wait_count, nconfirmed_count],
        }
        df_plot = pd.DataFrame(data)

        sns.barplot(data=df_plot, x="หมวดหมู่", y="จำนวน", palette="coolwarm", ax=ax)
        ax.set_title("เปรียบเทียบการลงทะเบียนและผลการจองนัดหมาย")
        plt.xticks(ha="center")
        add_value_labels(ax)
        plt.tight_layout()
        st.pyplot(fig)

    with tab2:
        st.header("การนัดหมายตามประเภทแพทย์")

        data_confirmed = df_username[df_username["ผลการนัดหมาย"] == "ยืนยันการจองนัดหมาย"]
        heart_doctor_count = (
            data_confirmed["แพทย์หัวใจ"].replace("", np.nan).notna().sum()
        )
        eye_doctor_count = data_confirmed["แพทย์ตา"].replace("", np.nan).notna().sum()
        general_doctor_count = (
            data_confirmed["แพทย์ทั่วไป"].replace("", np.nan).notna().sum()
        )
        cervical_doctor_count = (
            data_confirmed["แพทย์ปากมดลูก"].replace("", np.nan).notna().sum()
        )

        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("แพทย์หัวใจ", f"{heart_doctor_count:,}")
        with col2:
            st.metric("แพทย์ตา", f"{eye_doctor_count:,}")
        with col3:
            st.metric("แพทย์ทั่วไป", f"{general_doctor_count:,}")
        with col4:
            st.metric("แพทย์ปากมดลูก", f"{cervical_doctor_count:,}")

        # Create bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        data_counts = {
            "หมวดหมู่": ["แพทย์หัวใจ", "แพทย์ตา", "แพทย์ทั่วไป", "แพทย์ปากมดลูก"],
            "จำนวน": [
                heart_doctor_count,
                eye_doctor_count,
                general_doctor_count,
                cervical_doctor_count,
            ],
        }
        df_counts = pd.DataFrame(data_counts)

        sns.barplot(data=df_counts, x="หมวดหมู่", y="จำนวน", palette="coolwarm", ax=ax)
        ax.set_title("จำนวนผู้ป่วยที่มีการนัดหมายกับแพทย์แต่ละประเภท")
        plt.xticks(ha="center")
        add_value_labels(ax)
        plt.tight_layout()
        st.pyplot(fig)

    with tab3:
        st.header("การนัดหมายตามวัน")

        thai_days = {
            "Monday": "วันจันทร์",
            "Tuesday": "วันอังคาร",
            "Wednesday": "วันพุธ",
            "Thursday": "วันพฤหัสบดี",
            "Friday": "วันศุกร์",
            "Saturday": "วันเสาร์",
            "Sunday": "วันอาทิตย์",
        }
        thai_days_order = [
            "วันจันทร์",
            "วันอังคาร",
            "วันพุธ",
            "วันพฤหัสบดี",
            "วันศุกร์",
            "วันเสาร์",
            "วันอาทิตย์",
        ]

        data_confirmed = df_username[df_username["ผลการนัดหมาย"] == "ยืนยันการจองนัดหมาย"]
        data_confirmed["วัน"] = data_confirmed["วัน"].map(thai_days)

        # Create day counts dictionary for all days, including zeros for missing days
        day_counts_dict = {day: 0 for day in thai_days_order}
        temp_counts = data_confirmed["วัน"].value_counts().to_dict()
        day_counts_dict.update(temp_counts)

        # Create metrics for each day
        cols = st.columns(7)
        for i, (day, count) in enumerate(day_counts_dict.items()):
            with cols[i]:
                emoji_map = {
                    "วันจันทร์": "📅",
                    "วันอังคาร": "📅",
                    "วันพุธ": "📅",
                    "วันพฤหัสบดี": "📅",
                    "วันศุกร์": "📅",
                    "วันเสาร์": "📅",
                    "วันอาทิตย์": "📅",
                }
                st.metric(f"{emoji_map[day]} {day}", f"{count:,}")

        # Create bar chart
        day_counts = pd.DataFrame(
            {
                "วัน": list(day_counts_dict.keys()),
                "จำนวน": list(day_counts_dict.values()),
            }
        )

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=day_counts, x="วัน", y="จำนวน", palette="coolwarm", ax=ax)
        ax.set_title("จำนวนการนัดหมายในแต่ละวัน")
        plt.xticks(ha="center")
        add_value_labels(ax)
        plt.tight_layout()
        st.pyplot(fig)

else:
    st.error("ไม่สามารถโหลดข้อมูลได้ กรุณาตรวจสอบการเชื่อมต่อและไฟล์ข้อมูล")
