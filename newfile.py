# =============================================================
#  BezGranicVPN — полный исходный код проекта
#  Язык: JavaScript (Node.js) + библиотека Telegraf v4
#  Структура папок в Replit:
#    artifacts/telegram-bot/src/   — главный VPN-бот
#    artifacts/support-bot/src/    — бот поддержки
# =============================================================
#
#  Необходимые переменные окружения (Secrets):
#    BOT_TOKEN           — токен главного бота (@BezGranicVPN_bot)
#    SUPPORT_BOT_TOKEN   — токен бота поддержки (@BezGranicSupportbot)
#    CRYPTOPAY_TOKEN     — токен CryptoBot для оплаты USDT
#    ADMIN_TELEGRAM_ID   — Telegram ID администратора (число)
# =============================================================


# ─────────────────────────────────────────────────────────────
#  ФАЙЛ: artifacts/telegram-bot/src/config.js
# ─────────────────────────────────────────────────────────────
CONFIG_JS = r"""
export const config = {
  BOT_TOKEN: process.env.BOT_TOKEN,
  CRYPTOPAY_TOKEN: process.env.CRYPTOPAY_TOKEN,

  PRIVACY_POLICY_URL: 'https://telegra.ph/Politika-konfidencialnosti-04-01-26',
  USER_AGREEMENT_URL: 'https://telegra.ph/Polzovatelskoe-soglashenie-04-01-19',

  SUPPORT_BOT: '@BezGranicVPN_support',
  CHANNEL_USERNAME: '@BezGranicVPN',

  CRYPTOPAY_API_URL: 'https://pay.crypt.bot/api',

  PLANS: [
    {
      id: 'month_1',
      name: '🌙 1 месяц',
      price: 70,
      stars: 70,
      usdt: 0.91,
      description: '1 месяц доступа к BezGranicVPN',
      duration_days: 30,
    },
    {
      id: 'month_3',
      name: '⭐ 3 месяца',
      price: 180,
      stars: 180,
      usdt: 2.33,
      description: '3 месяца доступа к BezGranicVPN',
      duration_days: 90,
    },
    {
      id: 'year_1',
      name: '💎 1 год',
      price: 590,
      stars: 590,
      usdt: 7.65,
      description: '12 месяцев доступа к BezGranicVPN',
      duration_days: 365,
    },
  ],
};
"""


# ─────────────────────────────────────────────────────────────
#  ФАЙЛ: artifacts/telegram-bot/src/messages.js
# ─────────────────────────────────────────────────────────────
MESSAGES_JS = r"""
import { config } from './config.js';

export const messages = {
  welcome: (firstName) =>
    `👋 Привет, ${firstName}!\n\n` +
    `Добро пожаловать в <b>BezGranicVPN</b> — надёжный сервис для защиты вашего интернет-соединения.\n\n` +
    `🔒 Мы обеспечиваем:\n` +
    `• Безопасное шифрование трафика\n` +
    `• Высокую скорость соединения\n` +
    `• Работу на всех устройствах\n` +
    `• Круглосуточную поддержку\n\n` +
    `Выберите действие в меню ниже 👇`,

  choosePlan:
    `💰 <b>Доступные тарифы:</b>\n\n` +
    config.PLANS.map(p => `${p.name} — ${p.price}₽ / ${p.stars}⭐ / ${p.usdt} USDT`).join('\n') +
    `\n\n👇 Нажмите на тариф для оплаты`,

  choosePayment: (plan) =>
    `💳 <b>Способ оплаты</b>\n\n` +
    `Тариф: <b>${plan.name}</b>\n` +
    `• Telegram Stars: <b>${plan.stars} ⭐</b>\n` +
    `• USDT: <b>${plan.usdt} USDT</b>\n\n` +
    `Выберите удобный способ оплаты:`,

  usdtNoCryptobot:
    `💲 <b>Оплата USDT</b>\n\n` +
    `Для оплаты криптовалютой обратитесь в поддержку — мы предоставим актуальный адрес кошелька.`,

  noActiveSubscriptions:
    `📋 У вас пока нет активных подписок.\n\n` +
    `Нажмите «🌐 Купить подписку», чтобы выбрать тариф.`,

  documents:
    `📜 <b>Документы сервиса</b>\n\n` +
    `Ознакомьтесь с нашими документами:`,

  help:
    `❓ <b>Помощь и поддержка</b>\n\n` +
    `Если у вас возникли вопросы или проблемы — наша служба поддержки всегда готова помочь.\n\n` +
    `⏰ Время работы: с 9:00 до 21:00 (МСК)\n\n` +
    `📬 Пишите нам — мы отвечаем в течение нескольких часов.`,
};
"""


# ─────────────────────────────────────────────────────────────
#  ФАЙЛ: artifacts/telegram-bot/src/keyboards.js
# ─────────────────────────────────────────────────────────────
KEYBOARDS_JS = r"""
import { Markup } from 'telegraf';
import { config } from './config.js';

export function mainMenuKeyboard() {
  return Markup.keyboard([
    ['🌐 Купить подписку', '👤 Профиль'],
    ['❓ Помощь',          '📜 Документы'],
    ['📖 Инструкция',      '📣 Наш канал'],
  ]).resize();
}

export function instructionKeyboard() {
  return Markup.inlineKeyboard([
    [
      Markup.button.url('🤖 Скачать Android', 'https://play.google.com/store/apps/details?id=com.v2raytun.android'),
      Markup.button.url('🍎 Скачать iPhone',  'https://apps.apple.com/app/v2raytun/id6476628951'),
    ],
    [Markup.button.callback('← Назад', 'main_menu')],
  ]);
}

export function plansInlineKeyboard() {
  const buttons = config.PLANS.map((plan) => [
    Markup.button.callback(
      `${plan.name} — ${plan.price}₽ / ${plan.stars}⭐ / ${plan.usdt} USDT`,
      `plan_${plan.id}`
    ),
  ]);
  return Markup.inlineKeyboard(buttons);
}

export function paymentMethodKeyboard(plan) {
  return Markup.inlineKeyboard([
    [Markup.button.callback(`⭐ Telegram Stars — ${plan.stars}`, `pay_stars_${plan.id}`)],
    [Markup.button.callback(`💲 USDT — ${plan.usdt}`,           `pay_usdt_${plan.id}`)],
    [Markup.button.callback('← Назад', 'back_to_plans')],
  ]);
}

export function backToMainKeyboard() {
  return Markup.inlineKeyboard([
    [Markup.button.callback('← В главное меню', 'main_menu')],
  ]);
}

export function documentsKeyboard() {
  return Markup.inlineKeyboard([
    [Markup.button.url('📜 Политика конфиденциальности', config.PRIVACY_POLICY_URL)],
    [Markup.button.url('📋 Пользовательское соглашение', config.USER_AGREEMENT_URL)],
    [Markup.button.callback('← Назад', 'main_menu')],
  ]);
}

export function supportKeyboard() {
  return Markup.inlineKeyboard([
    [Markup.button.url('📩 Написать в поддержку', 'https://t.me/BezGranicSupportbot')],
    [Markup.button.callback('← Назад', 'main_menu')],
  ]);
}
"""


# ─────────────────────────────────────────────────────────────
#  ФАЙЛ: artifacts/telegram-bot/src/cryptopay.js
# ─────────────────────────────────────────────────────────────
CRYPTOPAY_JS = r"""
import { config } from './config.js';

export async function createUsdtInvoice({ amount, description, payload }) {
  if (!config.CRYPTOPAY_TOKEN) return null;

  const res = await fetch(`${config.CRYPTOPAY_API_URL}/createInvoice`, {
    method: 'POST',
    headers: {
      'Crypto-Pay-API-Token': config.CRYPTOPAY_TOKEN,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      asset: 'USDT',
      amount: String(amount),
      description,
      payload,
      paid_btn_name: 'callback',
      paid_btn_url: `https://t.me/${process.env.BOT_USERNAME || 'BezGranicVPN_bot'}`,
    }),
  });

  const data = await res.json();
  if (data.ok) return data.result;
  console.error('[CryptoPay] Ошибка:', data);
  return null;
}
"""


# ─────────────────────────────────────────────────────────────
#  ФАЙЛ: artifacts/telegram-bot/src/launcher.js
#  (тот же файл используется в support-bot/src/launcher.js)
# ─────────────────────────────────────────────────────────────
LAUNCHER_JS = r"""
export async function launchWithRetry(bot, name, maxRetries = 30) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      await bot.launch({ dropPendingUpdates: true });
      console.log(`✅ ${name} успешно запущен!`);
      return;
    } catch (err) {
      if (err.response?.error_code === 409 || err.message?.includes('409')) {
        const delay = Math.min((i + 1) * 3000, 15000);
        console.log(`⚠️ ${name}: конфликт (409), повтор через ${delay / 1000}с... (${i + 1}/${maxRetries})`);
        await new Promise((r) => setTimeout(r, delay));
      } else {
        throw err;
      }
    }
  }
  throw new Error(`${name}: не удалось запустить после ${maxRetries} попыток`);
}
"""


# ─────────────────────────────────────────────────────────────
#  ФАЙЛ: artifacts/telegram-bot/src/index.js  — ГЛАВНЫЙ БОТ
# ─────────────────────────────────────────────────────────────
INDEX_JS = r"""
import { Telegraf, session } from 'telegraf';
import { config } from './config.js';
import { messages } from './messages.js';
import { createUsdtInvoice } from './cryptopay.js';
import { launchWithRetry } from './launcher.js';
import {
  mainMenuKeyboard,
  plansInlineKeyboard,
  paymentMethodKeyboard,
  documentsKeyboard,
  supportKeyboard,
  backToMainKeyboard,
  instructionKeyboard,
} from './keyboards.js';

if (!config.BOT_TOKEN) {
  console.error('Ошибка: BOT_TOKEN не задан.');
  process.exit(1);
}

const bot = new Telegraf(config.BOT_TOKEN);

bot.use(session({ defaultSession: () => ({ pendingPlan: null }) }));

function getPlanById(planId) {
  return config.PLANS.find((p) => p.id === planId) || null;
}

function getUserBotId(telegramId) {
  return `VPN-${telegramId}`;
}

// /start
bot.start(async (ctx) => {
  await ctx.reply(messages.welcome(ctx.from.first_name), {
    parse_mode: 'HTML',
    ...mainMenuKeyboard(),
  });
});

// 🌐 Купить подписку
bot.hears('🌐 Купить подписку', async (ctx) => {
  await ctx.reply(messages.choosePlan, {
    parse_mode: 'HTML',
    ...plansInlineKeyboard(),
  });
});

// 👤 Профиль
bot.hears('👤 Профиль', async (ctx) => {
  const botId = getUserBotId(ctx.from.id);
  await ctx.reply(
    `👤 <b>Ваш профиль</b>\n\n` +
    `🆔 ID: <code>${botId}</code>\n` +
    `(нажмите на ID чтобы скопировать)\n\n` +
    `📋 Подписка: <b>Не активна</b>\n\n` +
    `Для покупки подписки нажмите «🌐 Купить подписку»`,
    { parse_mode: 'HTML', ...backToMainKeyboard() }
  );
});

// ❓ Помощь
bot.hears('❓ Помощь', async (ctx) => {
  await ctx.reply(messages.help, { parse_mode: 'HTML', ...supportKeyboard() });
});

// 📜 Документы
bot.hears('📜 Документы', async (ctx) => {
  await ctx.reply(messages.documents, { parse_mode: 'HTML', ...documentsKeyboard() });
});

// 📖 Инструкция
bot.hears('📖 Инструкция', async (ctx) => {
  await ctx.reply(
    `📖 <b>Инструкция по подключению</b>\n\n` +
    `<b>1.</b> Скачайте приложение <b>V2RayTun</b> (кнопки ниже)\n\n` +
    `<b>2.</b> Зайдите в раздел «👤 Профиль» в этом боте и скопируйте ключ подписки\n\n` +
    `<b>3.</b> В приложении V2RayTun нажмите кнопку <b>«Вставить из буфера обмена»</b> — подключение добавится автоматически\n\n` +
    `Если возникнут вопросы — обратитесь в поддержку 👇`,
    { parse_mode: 'HTML', ...instructionKeyboard() }
  );
});

// 📣 Наш канал
bot.hears('📣 Наш канал', async (ctx) => {
  const channelLink = `https://t.me/${config.CHANNEL_USERNAME.replace('@', '')}`;
  await ctx.reply(`📣 Подписывайтесь на наш канал:`, {
    reply_markup: {
      inline_keyboard: [[{ text: '📣 Перейти в канал', url: channelLink }]],
    },
  });
});

// Кнопка «← Назад» → планы
bot.action('back_to_plans', async (ctx) => {
  await ctx.answerCbQuery();
  await ctx.editMessageText(messages.choosePlan, {
    parse_mode: 'HTML',
    ...plansInlineKeyboard(),
  });
});

// Кнопка «В главное меню»
bot.action('main_menu', async (ctx) => {
  await ctx.answerCbQuery();
  await ctx.reply(`Главное меню 👇`, mainMenuKeyboard());
});

// Выбор тарифа
bot.action(/^plan_(.+)$/, async (ctx) => {
  await ctx.answerCbQuery();
  const planId = ctx.match[1];
  const plan = getPlanById(planId);
  if (!plan) return;
  ctx.session.pendingPlan = planId;
  await ctx.editMessageText(messages.choosePayment(plan), {
    parse_mode: 'HTML',
    ...paymentMethodKeyboard(plan),
  });
});

// Оплата Telegram Stars
bot.action(/^pay_stars_(.+)$/, async (ctx) => {
  await ctx.answerCbQuery();
  const planId = ctx.match[1];
  const plan = getPlanById(planId);
  if (!plan) return;
  await ctx.deleteMessage().catch(() => {});
  await ctx.replyWithInvoice({
    title: `BezGranicVPN — ${plan.name}`,
    description: plan.description,
    payload: `stars_${plan.id}_${ctx.from.id}`,
    currency: 'XTR',
    prices: [{ label: plan.name, amount: plan.stars }],
  });
});

// Оплата USDT через CryptoBot
bot.action(/^pay_usdt_(.+)$/, async (ctx) => {
  await ctx.answerCbQuery('Создаём счёт...');
  const planId = ctx.match[1];
  const plan = getPlanById(planId);
  if (!plan) return;

  if (!config.CRYPTOPAY_TOKEN) {
    await ctx.editMessageText(messages.usdtNoCryptobot, {
      parse_mode: 'HTML',
      reply_markup: {
        inline_keyboard: [
          [{ text: '📩 Написать в поддержку', url: `https://t.me/${config.SUPPORT_BOT.replace('@', '')}` }],
          [{ text: '← Назад', callback_data: `plan_${planId}` }],
        ],
      },
    });
    return;
  }

  const invoice = await createUsdtInvoice({
    amount: plan.usdt,
    description: `BezGranicVPN ${plan.name}`,
    payload: `usdt_${plan.id}_${ctx.from.id}`,
  });

  if (!invoice) {
    await ctx.editMessageText(messages.usdtNoCryptobot, {
      parse_mode: 'HTML',
      reply_markup: {
        inline_keyboard: [
          [{ text: '📩 Написать в поддержку', url: `https://t.me/${config.SUPPORT_BOT.replace('@', '')}` }],
          [{ text: '← Назад', callback_data: `plan_${planId}` }],
        ],
      },
    });
    return;
  }

  await ctx.editMessageText(
    `💲 <b>Оплата USDT через CryptoBot</b>\n\n` +
    `Тариф: <b>${plan.name} — ${plan.usdt} USDT</b>\n\n` +
    `Нажмите кнопку ниже для оплаты. Счёт действителен 1 час.`,
    {
      parse_mode: 'HTML',
      reply_markup: {
        inline_keyboard: [
          [{ text: `💲 Оплатить ${plan.usdt} USDT`, url: invoice.bot_invoice_url }],
          [{ text: '← Назад', callback_data: `plan_${planId}` }],
        ],
      },
    }
  );
});

// Telegram Stars — подтверждение перед списанием
bot.on('pre_checkout_query', async (ctx) => {
  await ctx.answerPreCheckoutQuery(true);
});

// Telegram Stars — успешная оплата
bot.on('successful_payment', async (ctx) => {
  const payment = ctx.message.successful_payment;
  const parts = payment.invoice_payload.split('_');
  const planId = parts[1] + '_' + parts[2];
  const plan = getPlanById(planId);

  console.log(`[Stars] Успешная оплата: ${ctx.from.id}, тариф: ${planId}, stars: ${payment.total_amount}`);

  await ctx.reply(
    `✅ <b>Оплата прошла успешно!</b>\n\n` +
    `Тариф: <b>${plan ? plan.name : planId}</b>\n` +
    `Оплачено: <b>${payment.total_amount} ⭐</b>\n\n` +
    `Ваша подписка активирована! Если возникнут вопросы — обращайтесь в поддержку.`,
    { parse_mode: 'HTML', ...backToMainKeyboard() }
  );
});

// Команды
bot.command('policy', async (ctx) => {
  await ctx.reply(`📜 Политика конфиденциальности:\n${config.PRIVACY_POLICY_URL}`);
});
bot.command('terms', async (ctx) => {
  await ctx.reply(`📋 Пользовательское соглашение:\n${config.USER_AGREEMENT_URL}`);
});
bot.command('help', async (ctx) => {
  await ctx.reply(messages.help, { parse_mode: 'HTML', ...supportKeyboard() });
});

bot.catch((err, ctx) => {
  console.error(`Ошибка при обработке ${ctx.updateType}:`, err);
});

console.log('VPN Бот запускается...');
launchWithRetry(bot, 'VPN Бот');

process.once('SIGINT',  () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
"""


# ─────────────────────────────────────────────────────────────
#  ФАЙЛ: artifacts/support-bot/src/index.js  — БОТ ПОДДЕРЖКИ
# ─────────────────────────────────────────────────────────────
SUPPORT_INDEX_JS = r"""
import { Telegraf, session } from 'telegraf';
import { launchWithRetry } from './launcher.js';

const BOT_TOKEN = process.env.SUPPORT_BOT_TOKEN;
const ADMIN_ID  = process.env.ADMIN_TELEGRAM_ID;

if (!BOT_TOKEN) {
  console.error('Ошибка: SUPPORT_BOT_TOKEN не задан.');
  process.exit(1);
}
if (!ADMIN_ID) {
  console.error('Ошибка: ADMIN_TELEGRAM_ID не задан.');
  process.exit(1);
}

const bot = new Telegraf(BOT_TOKEN);

bot.use(session({ defaultSession: () => ({}) }));

// /start
bot.start(async (ctx) => {
  await ctx.reply(
    `👋 Добро пожаловать в поддержку <b>BezGranicVPN</b>!\n\n` +
    `Напишите ваш вопрос или проблему прямо сейчас — мы ответим в течение <b>2 часов</b>.\n\n` +
    `🆔 Ваш ID: <code>VPN-${ctx.from.id}</code>`,
    { parse_mode: 'HTML', reply_markup: { remove_keyboard: true } }
  );
});

// Входящие сообщения — пересылаем администратору
bot.on('message', async (ctx) => {
  if (ctx.message.text?.startsWith('/')) return;

  const userId   = ctx.from.id;
  const username = ctx.from.username ? `@${ctx.from.username}` : 'без username';
  const firstName = ctx.from.first_name || '';
  const lastName  = ctx.from.last_name  || '';
  const botId    = `VPN-${userId}`;

  let adminMessage =
    `📩 <b>Сообщение в поддержку</b>\n\n` +
    `👤 ${firstName} ${lastName} (${username})\n` +
    `🆔 Telegram ID: <code>${userId}</code>\n` +
    `🆔 ID бота: <code>${botId}</code>\n\n` +
    `💬 Сообщение:\n`;

  try {
    if (ctx.message.text) {
      adminMessage += ctx.message.text;
      await bot.telegram.sendMessage(ADMIN_ID, adminMessage, { parse_mode: 'HTML' });
    } else if (ctx.message.photo) {
      adminMessage += '[фото]';
      await bot.telegram.sendMessage(ADMIN_ID, adminMessage, { parse_mode: 'HTML' });
      await bot.telegram.forwardMessage(ADMIN_ID, ctx.chat.id, ctx.message.message_id);
    } else if (ctx.message.document) {
      adminMessage += '[документ]';
      await bot.telegram.sendMessage(ADMIN_ID, adminMessage, { parse_mode: 'HTML' });
      await bot.telegram.forwardMessage(ADMIN_ID, ctx.chat.id, ctx.message.message_id);
    } else {
      adminMessage += '[медиа-сообщение]';
      await bot.telegram.sendMessage(ADMIN_ID, adminMessage, { parse_mode: 'HTML' });
      await bot.telegram.forwardMessage(ADMIN_ID, ctx.chat.id, ctx.message.message_id);
    }
  } catch (err) {
    console.error('[Support] Ошибка отправки сообщения админу:', err.message);
  }

  await ctx.reply(
    `✅ Ваше сообщение получено!\n\n` +
    `🆔 Ваш ID: <code>${botId}</code>\n\n` +
    `Мы ответим в течение <b>2 часов</b>.`,
    { parse_mode: 'HTML' }
  );

  console.log(`[Support] Сообщение от ${username} (${userId})`);
});

bot.catch((err, ctx) => {
  console.error(`[Support] Ошибка при обработке ${ctx.updateType}:`, err);
});

console.log('Бот поддержки запускается...');
launchWithRetry(bot, 'Бот поддержки');

process.once('SIGINT',  () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
"""


# ─────────────────────────────────────────────────────────────
#  ЗАВИСИМОСТИ: artifacts/telegram-bot/package.json
# ─────────────────────────────────────────────────────────────
PACKAGE_JSON = r"""
{
  "name": "@workspace/telegram-bot",
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "start": "node src/index.js"
  },
  "dependencies": {
    "telegraf": "^4.16.3"
  }
}
"""

SUPPORT_PACKAGE_JSON = r"""
{
  "name": "@workspace/support-bot",
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "start": "node src/index.js"
  },
  "dependencies": {
    "telegraf": "^4.16.3"
  }
}
"""
