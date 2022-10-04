import '~/pages/ocr.css';
import selectAll from '~/shared/selectAll';
import OcrApi from '~/api/OcrApi';
import Dialog from '~/shared/Dialog';
import Scissor from 'js-scissor';

async function getImageAsDataURL() {
  const resizeWidth = ref.compression.filter(':checked').val();
  if (resizeWidth)
    return (await new Scissor(ref.image.get(0)).resize(parseInt(resizeWidth, 10))).toBase64();
  const canvas = $('<canvas />').get(0);
  canvas.width = ref.image.get(0).naturalWidth;
  canvas.height = ref.image.get(0).naturalHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(ref.image.get(0), 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL('image/png', 1);
}

const ocrApi = new OcrApi();
const blockUI = new KTBlockUI(document.body, {
  message: 
    `<div class="blockui-message text-white">
      <span class="spinner-border text-primary h-20px w-20px me-2"></span>
      <span id="uploadProgress" class="fs-3">0</span>%...
    </div>`,
  overlayClass: "bg-dark bg-opacity-25"
});
const ref = selectAll();

ocrApi.onUploadProgress(percentCompleted => {
  $('#uploadProgress').text(percentCompleted);
});
$('body')
  .on('click', '[data-on-ocr]', async () => {
    try {
      blockUI.block();
      const type = ref.type.filter(':checked').val();
      const {data} = await ocrApi.ocr(type, await getImageAsDataURL());
      // console.log('data=', data);
      if (type === 'driverslicense') {
        ref.driverslicenseFullName.text(data.fullName);
        ref.driverslicenseFirstName.text(data.firstName);
        ref.driverslicenseLastName.text(data.lastName);
        ref.driverslicenseNumber.text(data.licenseNumber);
        ref.driverslicenseExpiryDate.text(data.expiryDate);
        // ref.driverslicenseWesternExpiryDate.text(data.wrnExpiryDate);
        ref.driverslicenseBirthday.text(data.birthday);
        ref.driverslicenseAge.text(data.age ? `${data.age}歳` : '');
        ref.driverslicenseWesternBirthday.text(data.wrnBirthday);
        // ref.driverslicensePostalCode.text(data.postalCode);
        ref.driverslicenseAddress.text(data.address);
      } else {
        ref.mynumberFullName.text(data.fullName);
        ref.mynumberFirstName.text(data.firstName);
        ref.mynumberLastName.text(data.lastName);
        ref.mynumberGender.text(data.gender);
        ref.mynumberCardExpiryDate.text(data.cardExpiryDate);
        // ref.mynumberWesternCardExpiryDate.text(data.wrnCardExpiryDate);
        ref.mynumberDigiExpiryDate.text(data.digiExpiryDate);
        // ref.mynumberWesternDigiExpiryDate.text(data.wrnDigiExpiryDate);
        ref.mynumberBirthday.text(data.birthday);
        ref.mynumberAge.text(data.age ? `${data.age}歳` : '');
        ref.mynumberWesternBirthday.text(data.wrnBirthday);
        // ref.mynumberPostalCode.text(data.postalCode);
        ref.mynumberAddress.text(data.address);
      }
      blockUI.release();
    } catch (err) {
      blockUI.release();
      await Dialog.unknownError();
      throw err;
    }
  })
  .on('change', '[data-on-change-type]', () => {
    const type = ref.type.filter(':checked').val();
    if (type === 'driverslicense') {
      for (let key of Object.keys(ref))
        if (key.match(/^driverslicense[A-Z][a-zA-Z]+/) && key !== 'driverslicenseOcrResults')
          ref[key].text('');
      ref.driverslicenseOcrResults.removeClass('d-none');
      ref.mynumberOcrResults.addClass('d-none');
      ref.image.attr('src', '/build/media/driverslicense.png');
    } else {
      for (let key of Object.keys(ref))
        if (key.match(/^mynumber[A-Z][a-zA-Z]+/) && key !== 'mynumberOcrResults')
          ref[key].text('');
      ref.driverslicenseOcrResults.addClass('d-none');
      ref.mynumberOcrResults.removeClass('d-none');
      ref.image.attr('src', '/build/media/mynumber.png');
    }
  })
  .on('change', '[data-on-upload-file]', evnt => {
    const reader = new FileReader();
    reader.onload = evnt => ref.image.attr('src', evnt.target.result);
    reader.readAsDataURL(evnt.currentTarget.files[0]);
  });