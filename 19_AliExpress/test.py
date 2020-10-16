country_list = ['Oman', 'Russian Federation', 'United States', 'Canada', 'Spain', 'France', 'United Kingdom', 'Netherlands', 'Israel',
                'Brazil', 'Chile', 'Australia', 'Ukraine', 'Belarus', 'Japan', 'Thailand', 'Singapore', 'Korea', 'Indonesia',
                'Malaysia', 'Philippines', 'Vietnam', 'Italy', 'Germany', 'Saudi Arabia', 'United Arab Emirates', 'Poland', 'Turkey', 'Portugal']
b = ['Afghanistan', 'Aland Islands', 'Albania', 'Alderney', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla',
     'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Ascension Island', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas',
     'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina',
     'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Caribbean Netherlands',
     'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros',
     'Congo, The Democratic Republic Of The', 'Congo, The Republic of Congo', 'Cook Islands', 'Costa Rica', "Cote D'Ivoire",
     'Croatia (local name: Hrvatska)', 'Curacao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic',
     'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)',
     'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'Gabon', 'Gambia', 'Georgia', 'Germany',
     'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau',
     'Guyana', 'Haiti', 'Honduras', 'Hong Kong,China', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iraq', 'Ireland', 'Israel', 'Italy',
     'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Korea', 'Kosovo', 'Kuwait', 'Kyrgyzstan',
     "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg',
     'Macau,China', 'Macedonia', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique',
     'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco',
     'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Negara Brunei Darussalam', 'Nepal', 'Netherlands', 'Netherlands Antilles',
     'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway',
     'Oman', 'Other Country', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines',
     'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Reunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthelemy',
     'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe',
     'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Netherlands)', 'Slovakia (Slovak Republic)',
     'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'South Sudan', 'Spain', 'Sri Lanka',
     'St. Pierre and Miquelon', 'Suriname', 'Swaziland', 'Sweden', 'Switzerland', 'Taiwan,China', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste',
     'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine',
     'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Vatican City State (Holy See)', 'Venezuela',
     'Vietnam', 'Virgin Islands (British)', 'Virgin Islands (U.S.)', 'Wallis And Futuna Islands', 'Yemen', 'Zambia', 'Zanzibar', 'Zimbabwe']
c = []
for item in country_list:
    c.append({
        "name": item,
        "index": b.index(item)
    })
print(c)