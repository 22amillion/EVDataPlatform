function fetchDataBefore2020() {
  fetch('/data_before_2020')
  .then(response => response.json())
  .then(data => {
    console.log('Data before 2020:', data);
  })
  .catch(error => console.error('Error fetching data before 2020:', error));
}

function fetchDataAfter2020() {
  fetch('/data_after_2020')
  .then(response => response.json())
  .then(data => {
    console.log('Data after 2020:', data);
  })
  .catch(error => console.error('Error fetching data after 2020:', error));
}

fetchDataBefore2020();
fetchDataAfter2020();

window.addEventListener('load', function() {
  var stateFilter = document.getElementById('stateFilter');
  var countyDropdown = document.getElementById('countyFilter');

  stateFilter.addEventListener('change', function() {
    var selectedState = this.value;
    countyDropdown.innerHTML = ''; 

    if (selectedState === 'Other') {
      var option = document.createElement('option');
      option.value = '';
      option.text = 'No county available';
      countyDropdown.appendChild(option);
      countyDropdown.disabled = true; 
      return; 
    } else {
      countyDropdown.disabled = false; 
    }

    var counties = getCountiesForState(selectedState);
    counties.forEach(function(county) {
      var option = document.createElement('option');
      option.value = county;
      option.text = county;
      countyDropdown.appendChild(option);
    });
  });
});

function getCountiesForState(state) {
  var countyData = {
    'WA': [
      'Adams', 'Asotin', 'Benton', 'Chelan', 'Clallam', 'Clark', 'Columbia', 'Cowlitz', 'Douglas', 'Ferry',
      'Franklin', 'Garfield', 'Grant', 'Grays Harbor', 'Island', 'Jefferson', 'King', 'Kitsap', 'Kittitas', 'Klickitat',
      'Lewis', 'Lincoln', 'Mason', 'Okanogan', 'Pacific', 'Pend Oreille', 'Pierce', 'San Juan', 'Skagit', 'Skamania',
      'Snohomish', 'Spokane', 'Stevens', 'Thurston', 'Wahkiakum', 'Walla Walla', 'Whatcom', 'Whitman', 'Yakima'
    ]
  };

  if (countyData.hasOwnProperty(state)) {
    return countyData[state];
  } else {
    return [];
  }
}

document.querySelectorAll('#yearFilter, #makeFilter, #stateFilter, #countyFilter')
.forEach(element => element.addEventListener('change', fetchFilteredData));

function fetchFilteredData() {
  const yearFilter = Array.from(document.getElementById('yearFilter').selectedOptions).map(option => option.value).join(',');
  const makeFilter = Array.from(document.getElementById('makeFilter').selectedOptions).map(option => option.value).join(',');
  const stateFilter = Array.from(document.getElementById('stateFilter').selectedOptions).map(option => option.value).join(',');
  const countyFilter = Array.from(document.getElementById('countyFilter').selectedOptions).map(option => option.value).join(',');

  const queryParams = new URLSearchParams({
    year: yearFilter,
    make: makeFilter,
    state: stateFilter,
    county: countyFilter
  });

  const apiUrl = `/filter_data?${queryParams}`;
  fetch(apiUrl)
    .then(response => response.json())
    .then(data => {
      const resultsBody = document.getElementById('searchResultsBody');
      resultsBody.innerHTML = '';  // Clear existing rows
      data.forEach(car => {
        const row = createTableRow(car);
        resultsBody.innerHTML += row;  // Add all new rows
      });
    })
    .catch(error => {
      console.error('Error fetching filtered data:', error);
      alert('Failed to fetch data. Please check your network connection and try again.');
    });
}

function createTableRow(car) {
  return `<tr>
    <td>${car["VIN (1-10)"]}</td>
    <td>${car.County}</td>
    <td>${car.City}</td>
    <td>${car.State}</td>
    <td>${car["Postal Code"]}</td>
    <td>${car.Year}</td>
    <td>${car.Make}</td>
    <td>${car.Model}</td>
    <td>${car.Type}</td>
    <td>${car.Eligibility}</td>
    <td>${car.Range} miles</td>
    <td>$${car.MSRP}</td>
  </tr>`;
}

document.getElementById('clearFilters').addEventListener('click', function() {
  document.getElementById('yearFilter').selectedIndex = -1;
  document.getElementById('makeFilter').selectedIndex = -1;
  document.getElementById('stateFilter').selectedIndex = -1;
  document.getElementById('countyFilter').selectedIndex = -1;
  const resultsBody = document.getElementById('searchResultsBody');
  resultsBody.innerHTML = '';  // Clear results table
});
