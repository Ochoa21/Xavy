function login() {
  const username = document.getElementById('login-username').value;
  const password = document.getElementById('login-password').value;

  fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  })
  .then(response => response.json())
  .then(data => {
    if (data.token) {
      localStorage.setItem('token', data.token);
      if (data.qrCode) {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('otp-form').style.display = 'block';
        const qrCodeImg = document.createElement('img');
        qrCodeImg.src = data.qrCode;
        document.getElementById('otp-form').appendChild(qrCodeImg);
      } else {
        alert('Inicio de sesión exitoso');
        document.getElementById('block-url-form').style.display = 'block';
        fetchBlockedUrls();
      }
    } else {
      alert(data.message);
    }
  })
  .catch(error => console.error('Error:', error));
}

function verifyOtp() {
  const otp = document.getElementById('otp').value;

  fetch('/verify-otp', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': localStorage.getItem('token') },
    body: JSON.stringify({ otp })
  })
  .then(response => response.json())
  .then(data => {
    if (data.message === 'OTP verificado con éxito') {
      alert('OTP verificado con éxito');
      document.getElementById('otp-form').style.display = 'none';
      document.getElementById('block-url-form').style.display = 'block';
      fetchBlockedUrls();
    } else {
      alert('OTP incorrecto');
    }
  })
  .catch(error => console.error('Error:', error));
}

function register() {
  const username = document.getElementById('register-username').value;
  const password = document.getElementById('register-password').value;
  const ownerKey = document.getElementById('owner-key').value;

  fetch('/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password, ownerKey })
  })
  .then(response => response.text())
  .then(message => {
    alert(message);
  })
  .catch(error => console.error('Error:', error));
}

function blockUrl() {
  const url = document.getElementById('block-url').value;

  fetch('/block', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Authorization': localStorage.getItem('token') },
    body: JSON.stringify({ url })
  })
  .then(response => response.text())
  .then(message => {
    alert(message);
    fetchBlockedUrls();
  })
  .catch(error => console.error('Error:', error));
}

function fetchBlockedUrls() {
  fetch('/blocked-urls', {
    headers: { 'Authorization': localStorage.getItem('token') }
  })
  .then(response => response.json())
  .then(urls => {
    const urlList = document.getElementById('blocked-urls');
    urlList.innerHTML = '';
    urls.forEach(url => {
      const li = document.createElement('li');
      li.textContent = url;
      urlList.appendChild(li);
    });
  });
}
