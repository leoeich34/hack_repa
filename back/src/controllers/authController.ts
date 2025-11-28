import { Request, Response } from 'express';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

const SECRET_KEY = 'alfa-hackathon-secret-key'; // В идеале в .env

// Имитация базы данных пользователей
const users: any[] = [];

export const authController = {
  // Регистрация
  async register(req: Request, res: Response) {
    try {
      const { email, password, name } = req.body;

      if (users.find(u => u.email === email)) {
        return res.status(400).json({ message: 'Пользователь уже существует' });
      }

      const hashedPassword = await bcrypt.hash(password, 10);
      const newUser = {
        id: Date.now().toString(),
        email,
        password: hashedPassword,
        name: name || 'Сотрудник'
      };

      users.push(newUser);

      // Сразу генерируем токен
      const token = jwt.sign({ id: newUser.id, email: newUser.email }, SECRET_KEY, { expiresIn: '24h' });

      res.json({ token, user: { id: newUser.id, email: newUser.email, name: newUser.name } });
    } catch (e) {
      res.status(500).json({ message: 'Ошибка сервера' });
    }
  },

  // Вход
  async login(req: Request, res: Response) {
    try {
      const { email, password } = req.body;
      const user = users.find(u => u.email === email);

      if (!user) {
        return res.status(400).json({ message: 'Неверный логин или пароль' });
      }

      const isValid = await bcrypt.compare(password, user.password);
      if (!isValid) {
        return res.status(400).json({ message: 'Неверный логин или пароль' });
      }

      const token = jwt.sign({ id: user.id, email: user.email }, SECRET_KEY, { expiresIn: '24h' });

      res.json({ token, user: { id: user.id, email: user.email, name: user.name } });
    } catch (e) {
      res.status(500).json({ message: 'Ошибка сервера' });
    }
  },

  // Проверка текущего пользователя
  async me(req: Request, res: Response) {
      // Для простоты хакатона просто возвращаем ОК, если токен валиден (проверяем на фронте)
      // В реальности тут middleware
      res.json({ status: 'ok' });
  },

  async updateProfile(req: Request, res: Response) {
    try {
      // Получаем токен из заголовка (упрощенно для хакатона)
      const token = req.headers.authorization?.split(' ')[1];
      if (!token) return res.status(401).json({ message: 'Нет доступа' });

      // Декодируем (в реальности это делает middleware)
      const decoded: any = jwt.verify(token, SECRET_KEY);

      // Ищем юзера в нашей "базе"
      const user = users.find(u => u.id === decoded.id);

      if (!user) {
        return res.status(404).json({ message: 'Пользователь не найден' });
      }

      // Обновляем поля
      const { name, position, department } = req.body;
      if (name) user.name = name;
      if (position) user.position = position;
      if (department) user.department = department;

      // Возвращаем обновленного юзера
      res.json({
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          position: user.position || 'Стажер',
          department: user.department || 'Отдел продаж'
        }
      });
    } catch (e) {
      console.log(e)
      res.status(500).json({ message: 'Ошибка обновления' });
    }
  }
};