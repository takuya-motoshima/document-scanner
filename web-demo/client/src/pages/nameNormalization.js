import '~/pages/nameNormalization.css';
import NameNormalizationApi from '~/api/NameNormalizationApi';
import trim from '~/shared/trim';
import splitNewLine from '~/shared/splitNewLine';

const nameNormalizationApi = new NameNormalizationApi();
const inputs = document.querySelector('#inputs');
const form = document.querySelector('#form');
const submit = form.querySelector('[type="submit"]');
const spinner = submit.querySelector('.spinner-border');
const table = document.querySelector('#table > tbody');

inputs.addEventListener('input', () => {
  const value = trim(inputs.value);
  submit.disabled = value === '';
  if (!value)
    return void (table.innerHTML = '');
  const rows = splitNewLine(inputs.value);
  const fragment = document.createDocumentFragment();
  for (let [i, value] of Object.entries(rows)) {
    const row = document.createElement('tr');
    const cellNo = document.createElement('td');
    cellNo.classList.add('ps-9');
    cellNo.textContent = `#${parseInt(i, 10) + 1}`;
    const cellFullname = document.createElement('td');
    cellFullname.textContent = value;
    const cellScore = document.createElement('td');
    cellScore.classList.add('text-end');
    row.appendChild(cellNo);
    row.appendChild(cellFullname);
    row.appendChild(document.createElement('td'));
    row.appendChild(document.createElement('td'));
    row.appendChild(cellScore);
    fragment.appendChild(row);
  }
  table.innerHTML = '';
  table.appendChild(fragment);
}, {passive: true});

form.addEventListener('submit', async evnt => {
  try {
    evnt.preventDefault();
    spinner.classList.remove('d-none');
    const promises = [];
    for (let row of table.querySelectorAll('tr')) {
      promises.push((row => {
        return new Promise(async (rslv, rej) => {
          const cellLastName = row.querySelector('td:nth-child(3)');
          const cellFirstName = row.querySelector('td:nth-child(4)');
          const cellScore = row.querySelector('td:nth-child(5)');
          cellLastName.textContent = cellFirstName.textContent = cellScore.textContent = '';
          try {
            cellLastName.innerHTML = `<div class="spinner-border spinner-border-sm" role="status"><span class="visually-hidden">Loading...</span></div>`;
            const {data} = await nameNormalizationApi.nameNormalization(row.querySelector('td:nth-child(2)').textContent);
            // console.log('data=', data);
            const score = parseFloat(data.score);
            const scorePercent = (score * 100).toFixed(2);
            cellScore.innerHTML = `<span class="fw-bold">${scorePercent}</span>%`;
            // cellScore.textContent = `${scorePercent}%`;
            if (data.firstName && data.score >= .2) {
              cellLastName.textContent = data.lastName;
              cellFirstName.textContent = data.firstName;
            } else
              cellLastName.innerHTML = '<span class="text-danger">Can\'t find</span>';
            rslv();
          } catch (err) {
            cellLastName.innerHTML = '<span class="text-danger">Error</span>';
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

inputs.dispatchEvent(new Event('input'));