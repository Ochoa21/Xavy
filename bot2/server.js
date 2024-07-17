require('dotenv').config();
const express = require('express');
const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const path = require('path');
const speakeasy = require('speakeasy');

const app = express();
app.use(express.json());

const JWT_SECRET = process.env.JWT_SECRET || 'mi_clave_secreta_jwt';
const PORT = process.env.PORT || 3000;

// Conectar a la base de datos MongoDB
mongoose.connect('mongodb://localhost:27017/gestor_colas', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Esquema y modelo de usuario
const userSchema = new mongoose.Schema({
  username: String,
  password: String,
  isAdmin: Boolean,
  otpSecret: String,
});

const User = mongoose.model('User', userSchema);

// Ruta para la raíz
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Middleware de autenticación JWT
const authenticateJWT = (req, res, next) => {
  const token = req.headers.authorization;
  if (token) {
    jwt.verify(token, JWT_SECRET, (err, user) => {
      if (err) {
        return res.sendStatus(403);
      }
      req.user = user;
      next();
    });
  } else {
    res.sendStatus(401);
  }
};

// Ruta de registro de usuario
app.post('/register', async (req, res) => {
  const { username, password, isAdmin } = req.body;
  const hashedPassword = bcrypt.hashSync(password, 8);

  const newUser = new User({
    username,
    password: hashedPassword,
    isAdmin,
    otpSecret: isAdmin ? null : speakeasy.generateSecret().base32,
  });

  await newUser.save();
  res.status(201).send('Usuario registrado');
});

// Ruta de inicio de sesión
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await User.findOne({ username });

  if (!user) {
    return res.status(401).send('Usuario no encontrado');
  }

  const passwordIsValid = bcrypt.compareSync(password, user.password);

  if (!passwordIsValid) {
    return res.status(401).send('Contraseña incorrecta');
  }

  if (user.isAdmin) {
    // Si el usuario es administrador, no requiere OTP
    const token = jwt.sign({ id: user._id, isAdmin: user.isAdmin }, JWT_SECRET, {
      expiresIn: '1h',
    });
    return res.json({ token });
  } else {
    // Si el usuario no es administrador, enviar el secreto OTP
    return res.json({ otpRequired: true, otpSecret: user.otpSecret });
  }
});

// Ruta para verificar OTP
app.post('/verify-otp', authenticateJWT, async (req, res) => {
  const { token } = req.body;
  const { otpSecret } = req.user;

  const verified = speakeasy.totp.verify({
    secret: otpSecret,
    encoding: 'base32',
    token,
  });

  if (verified) {
    const token = jwt.sign({ id: req.user._id, isAdmin: req.user.isAdmin }, JWT_SECRET, {
      expiresIn: '1h',
    });
    res.json({ token });
  } else {
    res.status(401).send('OTP incorrecta');
  }
});

// Ruta protegida de ejemplo
app.get('/protected', authenticateJWT, (req, res) => {
  res.send('Esta es una ruta protegida');
});

// Ruta principal
app.get('/', (req, res) => {
  res.send('¡Bienvenido al gestor de colas!');
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor ejecutándose en http://localhost:${PORT}`);
});

// Crear un usuario administrador por defecto
(async () => {
  const adminExists = await User.findOne({ username: 'admin' });

  if (!adminExists) {
    const hashedPassword = bcrypt.hashSync('admin123', 8);

    const adminUser = new User({
      username: 'admin',
      password: hashedPassword,
      isAdmin: true,
      otpSecret: null,
    });

    await adminUser.save();
    console.log('Usuario administrador creado: admin / admin123');
  }
})();
