from bs4 import BeautifulSoup
from helpers import simple_get, save_list_as_json


# https://www.hudhomestore.com/Listing/PropertySearchResult.aspx?pageId=2&sState=AK

def get_record_count(html_object):
    record_count_list = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblTotalNoRecords']
    record_count = record_count_list[0][:2] if record_count_list else 0
    return int(record_count)

def get_case_numbers_on_page(html_object):
    case_numbers = [l.text for l in html_object.select('label') if l['id'][:27] == 'ctl00_dgPropertyList_Label4']
    return case_numbers

def get_all_case_numbers_for_state(state_abbreviation):
    case_numbers = []
    page_index = 1

    url = f'https://www.hudhomestore.com/Listing/PropertySearchResult.aspx?pageId={page_index}&sState={state_abbreviation}'
    raw_html = simple_get(url)
    html = BeautifulSoup(raw_html, 'html.parser')
    record_count = get_record_count(html)
    case_numbers += get_case_numbers_on_page(html)

    while len(case_numbers) < record_count:
        page_index += 1
        url = f'https://www.hudhomestore.com/Listing/PropertySearchResult.aspx?pageId={page_index}&sState={state_abbreviation}'
        raw_html = simple_get(url)
        html = BeautifulSoup(raw_html, 'html.parser')
        case_numbers += get_case_numbers_on_page(html)

    return case_numbers

def get_all_case_numbers():
    case_numbers = []
    states = ['AA',	'AE',	'AE',	'AE',	'AE',	'AK',	'AL',	'AP',	'AR',	'AS',	'AZ',	'CA',	'CO',	'CT',	'DC',	'DE',	'FL',	'FM',	'GA',	'GU',	'HI',	'IA',	'ID',	'IL',	'IN',	'KS',	'KY',	'LA',	'MA',	'MD',	'ME',	'MH',	'MI',	'MN',	'MO',	'MP',	'MS',	'MT',	'NC',	'ND',	'NE',	'NH',	'NJ',	'NM',	'NV',	'NY',	'OH',	'OK',	'OR',	'PA',	'PR',	'PW',	'RI',	'SC',	'SD',	'TN',	'TX',	'UT',	'VA',	'VI',	'VT',	'WA',	'WI',	'WV',	'WY']
    for state in states:
        case_numbers += get_all_case_numbers_for_state(state)
    print(len(case_numbers))
    return case_numbers



def get_listing_data(case_number):
    url = f'https://www.hudhomestore.com/Listing/PropertyDetails.aspx?caseNumber={case_number}'
    raw_html = simple_get(url)
    html_object = BeautifulSoup(raw_html, 'html.parser')

    listing_data = {}
    listing_data['address'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblAddress'][0]
    listing_data['bed_bath'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblBedBath'][0]
    listing_data['room_count'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblTotalRooms'][0]
    listing_data['sq_feet'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblSqft'][0]
    listing_data['build_year'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblYear'][0]
    listing_data['house_type'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblHousingType'][0]
    listing_data['story_count'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblStories'][0]
    listing_data['hoa_fee'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblHOAFees'][0]
    listing_data['is_revitalization_area'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblRevitArea'][0]
    listing_data['lot_size'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblAcreage'][0]
    listing_data['list_date'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblListdate'][0]
    listing_data['period_type'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblBidPeriod'][0]
    listing_data['period_deadline'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblBidDeadline'][0]
    listing_data['price'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblPrice'][0]
    listing_data['fha_financing_type'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblFHA'][0]
    listing_data['is_203k_eligible'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblEligible'][0]
    listing_data['bidder_type'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblBidPeriodTop'][0]
    listing_data['bid_deadline'] = [span.text for span in html_object.select('span') if span.get('id') == 'ctl00_lblBidDeadlineTop'][0]

    return listing_data

def get_all_listing_data(case_number_list):
    all_listings_data = []

    for case_number in case_number_list:
        listing_data = get_listing_data(case_number)
        all_listings_data.append(listing_data)

    return all_listings_data
    
def update_and_save_hud_listing_data():
    case_numbers = get_all_case_numbers()
    save_list_as_json(case_numbers,'case_numbers')
    
    listings_data = get_all_listing_data(case_numbers)
    save_list_as_json(listings_data, 'listings_data')


if __name__ == '__main__':
    update_and_save_hud_listing_data()
