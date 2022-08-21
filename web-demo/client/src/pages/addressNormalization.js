import '~/pages/addressNormalization.css';
import AddressNormalizationApi from '~/api/AddressNormalizationApi';

const addressNormalizationApi = new AddressNormalizationApi();
const inputs = document.querySelector('#inputs');
const form = document.querySelector('#form');
const submit = form.querySelector('[type="submit"]');
const spinner = submit.querySelector('.spinner-border');
const table = document.querySelector('#table > tbody');

// Activate submit if there is input.
inputs.addEventListener('input', () => {
  // Remove spaces before and after each line from the input value.
  const value = inputs.value.replace(/\r?\n/g, '').replace(/^[\s　]+|[\s　]+$/g, '');

  // Activate submit if there is input.
  submit.disabled = value === '';

  // If there is no input, empty the table and finish.
  if (!value)
    return void (table.innerHTML = '');

  // Split the input value into lines.
  const rows = inputs.value
    .replace(/^[\s　]*\r?\n/gm, '')     // Remove blank lines.
    .replace(/\r?\n$/, '')              // Removed trailing line breaks.
    .replace(/^[\s　]+|[\s　]+$/gm, '') // Trim the space in each row.
    .split(/\r?\n/);

  // Display the entered address in the table.
  const fragment = document.createDocumentFragment();
  for (let [i, value] of Object.entries(rows)) {
    const row = document.createElement('tr');
    const cellNo = document.createElement('td');
    cellNo.classList.add('ps-9');
    cellNo.textContent = `#${parseInt(i, 10) + 1}`;
    const cellAddress = document.createElement('td');
    const cellPref = document.createElement('td');
    const cellCity = document.createElement('td');
    const cellTown = document.createElement('td');
    const cellAddr = document.createElement('td');
    cellAddress.textContent = value;
    row.appendChild(cellNo);
    row.appendChild(cellAddress);
    row.appendChild(cellPref);
    row.appendChild(cellCity);
    row.appendChild(cellTown);
    row.appendChild(cellAddr);
    fragment.appendChild(row);
  }
  table.innerHTML = '';
  table.appendChild(fragment);
}, {passive: true});

// Submit.
form.addEventListener('submit', async evnt => {
  try {
    evnt.preventDefault();
    spinner.classList.remove('d-none');
    const promises = [];
    for (let row of table.querySelectorAll('tr')) {
      promises.push((row => {
        return new Promise(async (rslv, rej) => {
          const cellPref = row.querySelector('td:nth-child(3)');
          const cellCity = row.querySelector('td:nth-child(4)');
          const cellTown = row.querySelector('td:nth-child(5)');
          const cellAddr = row.querySelector('td:nth-child(6)');
          try {
            // Show loading.
            cellPref.innerHTML = `<div class="spinner-border spinner-border-sm" role="status">
                                <span class="visually-hidden">Loading...</span>
                              </div>`

            // Send request.
            const {data} = await addressNormalizationApi.addressNormalization(row.querySelector('td:nth-child(2)').textContent);
            cellPref.innerHTML = data.pref;
            cellCity.innerHTML = data.city;
            cellTown.innerHTML = data.town;
            cellAddr.innerHTML = data.addr;
            rslv();
          } catch (err) {
            cellPref.innerHTML = '<span class="text-danger">Can\'t split</span>';
            rej(err);
          }
        });
      })(row));
    }
    await Promise.all(promises)
  } catch (err) {
    alert(err.message);
  } finally {
    spinner.classList.add('d-none');
  }
}, {passive: false});

// Fire input event.
inputs.dispatchEvent(new Event('input'));