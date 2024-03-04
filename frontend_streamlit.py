import streamlit as st
import requests

st.title('Distance Calculator')
st.subheader('Enter 3 addresses (or postal codes) in Singapore and find out which two locations are closest, and the travel time and distance between them by car.', divider='rainbow')

address_1 = st.text_input('Enter first address or postal code: ', '')
address_2 = st.text_input('Enter second address or postal code: ', '')
address_3 = st.text_input('Enter third address or postal code: ', '')

if st.button('Calculate'):
    response = requests.post('http://127.0.0.1:8000/distance/', json={'address_1': address_1, 'address_2': address_2, 'address_3': address_3})
    if response.status_code == 200:
        data = response.json()
        st.write(data['message'])
        
        if 'addresses' in data:
            st.write('Addresses:', data['addresses'])
            
        st.write('Distances:', data['distances'])
        st.write('Durations:', data['durations'])
        
        # Finding the closest locations and their travel time.
        distances_float = {key: float(value.split()[0]) for key, value in data['distances'].items()}

        # Find the key with the minimum distance
        min_distance_key = min(distances_float, key=distances_float.get)
        loc1, loc2 = min_distance_key.split('-')
        duration = data['durations'].get(min_distance_key)

        st.subheader(f'The closest locations are {loc1} and {loc2}, and the travel time between them is {duration}.')
    else:
        st.error('Error processing request') 