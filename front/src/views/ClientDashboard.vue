<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { apiClient, type PredictionResponse } from '../services/apiClient'
import Income3DCard from '../components/Income3DCard.vue'
import SimulatorPanel from '../components/SimulatorPanel.vue'
import { useNotification } from '../composables/useNotification'
// @ts-ignore
import html2pdf from 'html2pdf.js'

import {
  BriefcaseIcon, CreditCardIcon, CheckBadgeIcon,
  ArrowPathIcon, ExclamationTriangleIcon, TableCellsIcon,
  ChartBarIcon, DocumentArrowDownIcon,
  HomeIcon, BanknotesIcon, ShieldCheckIcon, DevicePhoneMobileIcon
} from '@heroicons/vue/24/outline'

import {
  Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale, PointElement, LineElement
} from 'chart.js'
import { Bar, Line } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend, PointElement, LineElement)

const route = useRoute()
const { show } = useNotification()
const loading = ref(true)
const pdfLoading = ref(false)
const data = ref<any>(null)
const error = ref(false)
const simulatedData = ref<any>(null)
const isDetailedMode = ref(false)

// --- 1. ГЛОБАЛЬНЫЙ СЛОВАРЬ ПЕРЕВОДА ---
const featureDictionary: Record<string, string> = {
  // Личные данные
  'age': 'Возраст клиента',
  'gender': 'Пол',
  'adminarea': 'Регион проживания',
  'city_smart_name': 'Город',
  'nonresident_flag': 'Нерезидент',
  'mob_cnt_days': 'Активность в приложении (дни)',
  'mob_total_sessions': 'Сессий в приложении',
  'lifetimeComp': 'Срок жизни счета',
  'client_active_flag': 'Активный клиент',

  // Доходы
  'incomeValue': 'Подтвержденный доход',
  'incomeValueCategory': 'Категория дохода',
  'salary_6to12m_avg': 'Средняя зарплата (6-12 мес)',
  'first_salary_income': 'Первый доход (ЗП проект)',
  'per_capita_income_rur_amt': 'Средний доход в регионе',
  'salary_median_in_gex_r1': 'Медианная ЗП в локации',
  'profit_income_out_rur_amt_12m': 'Прибыль (12 мес)',
  'profit_income_out_rur_amt_l2m': 'Прибыль (2 мес)',

  // FE (Расчетные)
  'fe_salary_6to12_to_ils_3y': 'Динамика зарплаты (3г)',
  'fe_bki_total_debt': 'Общий долг (FE)',
  'fe_bki_utilization': 'Утилизация лимитов',
  'fe_bki_limit_per_product': 'Средний лимит на продукт',

  // Балансы
  'avg_balance_rur_amt_1m_af': 'Средний баланс (1 мес)',
  'max_balance_rur_amt_1m_af': 'Макс. баланс (1 мес)',
  'min_balance_rur_amt_1m_af': 'Мин. баланс (1 мес)',
  'curr_rur_amt_cm_avg': 'Текущий средний остаток',
  'total_sum': 'Общая сумма средств',

  // Кредиты
  'loan_cur_amt': 'Текущая сумма кредитов',
  'loan_cnt': 'Количество кредитов',
  'other_credits_count': 'Кредиты в других банках',
  'ovrd_sum': 'Сумма просрочки',

  // Обороты
  'turn_cur_cr_avg_act_v2': 'Активность поступлений',
  'avg_cur_cr_turn': 'Кредитовые обороты (ср.)',
  'turn_cur_cr_max_v2': 'Макс. поступления',
  'turn_cur_cr_avg_v2': 'Средние поступления',
  'turn_cur_cr_sum_v2': 'Сумма поступлений',
  'turn_cur_cr_7avg_avg_v2': 'Поступления (скользящ.)',
  'avg_fdep_cr_turn': 'Пополнения вкладов',
  'avg_cur_db_turn': 'Списания по картам',
  'turn_cur_db_max_v2': 'Макс. списание',
  'turn_cur_db_sum_v2': 'Сумма списаний',
  'turn_cur_db_avg_act_v2': 'Активность списаний',

  // Категории
  'transaction_category_supermarket_sum_cnt_m2': 'Транзакции: Супермаркеты',
  'transaction_category_fastfood_percent_cnt_2m': 'Доля трат: Фастфуд',
  'transaction_category_restaurants_sum_amt_m2': 'Траты: Рестораны',
  'transaction_category_cash_percent_amt_2m': 'Доля снятия наличных',
  'summarur_1m_purch': 'Покупки за месяц',

  // Специфичные категории (быстрый перевод)
  'amount_by_category_90d__summarur_amt__sum__cashflowcategory_name__elektronnye_dengi': 'Траты: Электронные деньги',
  'amount_by_category_90d__summarur_amt__sum__cashflowcategory_name__vydacha_nalichnyh_v_bankomate': 'Снятие наличных (90 дн)',

  // СБП и переводы
  'by_category__amount__sum__eoperation_type_name__vhodjaschij_bystryj_platezh_sbp': 'Входящие СБП',
  'by_category__amount__sum__eoperation_type_name__ishodjaschij_bystryj_platezh_sbp': 'Исходящие СБП',
  'by_category__amount__sum__eoperation_type_name__perevod_s_karty_na_kartu': 'P2P Переводы',
  'by_category__amount__sum__eoperation_type_name__perevod_mezhdu_svoimi_schetami': 'Переводы между счетами',
  'by_category__amount__sum__eoperation_type_name__perevod_po_nomeru_telefona': 'Переводы по телефону',
  'by_category__amount__sum__eoperation_type_name__platezh_za_mobilnyj_cherez_ps': 'Оплата мобильного',

  // БКИ детально
  'hdb_bki_total_cc_max_limit': 'Лимит кредиток (БКИ)',
  'hdb_bki_total_max_limit': 'Общий кредитный лимит',
  'fe_bki_total_limit': 'Кредитная нагрузка (Расч.)',
  'hdb_bki_total_pil_max_limit': 'Лимит потреб. кредитов',
  'hdb_bki_total_products': 'Всего кредитных счетов',
  'hdb_bki_active_cc_max_limit': 'Лимит активной кредитки',
  'bki_total_max_limit': 'Макс. лимит БКИ'
}

const getFeatureName = (techName: string) => {
  if (featureDictionary[techName]) return featureDictionary[techName]
  let name = techName

  // Универсальные парсеры для длинных имен

  // 1. Transaction Category
  if (name.includes('transaction_category')) return 'Транзакционная активность'

  // 2. Cashflow Category (amount_by_category...)
  if (name.includes('cashflowcategory_name')) {
      if (name.includes('vydacha_nalichnyh')) return 'Выдача наличных'
      if (name.includes('perevod')) return 'Переводы'
      if (name.includes('supermarkety') || name.includes('supermarketov')) return 'Категория: Супермаркеты'
      if (name.includes('kafe')) return 'Категория: Кафе'
      if (name.includes('odezhda')) return 'Категория: Одежда'
      if (name.includes('oteli')) return 'Категория: Отели'
      if (name.includes('produkty')) return 'Категория: Продукты'
      if (name.includes('puteshestvija')) return 'Категория: Путешествия'
      if (name.includes('reklama')) return 'Категория: Реклама'
      if (name.includes('elektronnye_dengi')) return 'Электронные деньги'
      if (name.includes('zarubezhnye')) return 'Зарубежные операции'
      if (name.includes('kosmetika')) return 'Категория: Косметика'
      if (name.includes('gipermarkety')) return 'Категория: Гипермаркеты'
      if (name.includes('platezhi_cherez_internet')) return 'Интернет платежи'
      return 'Категория трат'
  }

  // 3. By Category (eoperation)
  if (name.includes('by_category__amount__sum')) {
      if (name.includes('perevod')) return 'Операции перевода'
      if (name.includes('platezh')) return 'Платежные операции'
      if (name.includes('sbp')) return 'Операции СБП'
      return 'Сумма по категории'
  }

  // 4. БКИ
  if (name.includes('hdb_bki') || name.includes('bki_total')) return 'Данные БКИ'

  // 5. Обороты
  if (name.includes('turn_cur')) return 'Обороты по счету'

  // Фоллбек
  return name.replace(/_/g, ' ').substring(0, 25)
}

// --- 2. ПОЛНЫЙ КАТАЛОГ ПРОДУКТОВ (18 шт) ---
const PRODUCT_CATALOG = [
    // === PREMIUM ===
    {
        id: 'alfa_only', type: 'INVEST', title: 'Alfa Only',
        text: 'Премиальное обслуживание, бизнес-залы, консьерж и кэшбэк до 100%.',
        rules: (inc: number, pdn: number) => (inc > 250000 ? 150 : -1)
    },
    {
        id: 'invest_private', type: 'INVEST', title: 'А-Инвестиции Private',
        text: 'Персональный брокер и стратегии для капитала от 5 млн ₽.',
        rules: (inc: number, pdn: number) => (inc > 300000 ? 120 : -1)
    },

    // === ИПОТЕКА ===
    {
        id: 'mortgage_priv', type: 'MORTGAGE', title: 'Ипотека с господдержкой',
        text: 'Ставка от 6%. Лимит до 30 млн ₽. Оформление онлайн.',
        rules: (inc: number, pdn: number) => (inc > 100000 && pdn < 50 ? 85 : 0)
    },
    {
        id: 'mortgage_it', type: 'MORTGAGE', title: 'IT-Ипотека',
        text: 'Специальная ставка 5% для сотрудников IT-компаний.',
        rules: (inc: number, pdn: number) => (inc > 150000 && pdn < 45 ? 95 : 0)
    },

    // === АВТО ===
    {
        id: 'auto_new', type: 'CASH_LOAN', title: 'Автокредит на новое',
        text: 'Без первоначального взноса. Ставка от 14%.',
        rules: (inc: number, pdn: number) => (inc > 80000 && pdn < 60 ? 75 : 0)
    },
    {
        id: 'auto_used', type: 'CASH_LOAN', title: 'Авто с пробегом',
        text: 'Покупка у частного лица или дилера. Проверка авто бесплатно.',
        rules: (inc: number, pdn: number) => (inc > 50000 && inc < 120000 && pdn < 55 ? 65 : 0)
    },

    // === КРЕДИТНЫЕ КАРТЫ ===
    {
        id: 'credit_365', type: 'CREDIT_CARD', title: 'Год без %',
        text: 'Главная кредитка страны. 365 дней без процентов на покупки.',
        rules: (inc: number, pdn: number) => (inc > 30000 && pdn < 70 ? 90 : 10)
    },
    {
        id: 'travel_credit', type: 'CREDIT_CARD', title: 'Alfa Travel Credit',
        text: 'Милли за покупки. Бесплатная страховка для путешественников.',
        rules: (inc: number, pdn: number) => (inc > 100000 ? 70 : 0)
    },

    // === КРЕДИТЫ И РЕФИНАНС ===
    {
        id: 'cash_loan', type: 'CASH_LOAN', title: 'Кредит наличными',
        text: 'Деньги на любые цели. Решение за 2 минуты.',
        rules: (inc: number, pdn: number) => (pdn < 50 && inc > 40000 ? 80 : -10)
    },
    {
        id: 'refinance', type: 'REFINANCE', title: 'Рефинансирование',
        text: 'Объедините кредиты в один. Уменьшите платеж на 30%.',
        rules: (inc: number, pdn: number) => (pdn > 50 ? 250 : 0) // Топ при нагрузке
    },
    {
        id: 'installment', type: 'INSTALLMENT', title: 'Карта рассрочки',
        text: 'Покупки сейчас, оплата частями 0-0-12.',
        rules: (inc: number, pdn: number) => (inc < 60000 && pdn < 60 ? 60 : 20)
    },

    // === ДЕБЕТОВЫЕ ===
    {
        id: 'kids_card', type: 'DEBIT', title: 'Детская карта',
        text: 'Приложение для ребенка, кэшбэк в кафе и контроль трат.',
        rules: (inc: number, pdn: number) => (inc > 70000 && pdn < 40 ? 45 : 0)
    },
    {
        id: 'alfa_pay', type: 'DEBIT', title: 'Платежное кольцо',
        text: 'Оплата касанием. Керамика, водонепроницаемое.',
        rules: (inc: number, pdn: number) => (inc > 180000 ? 50 : -100)
    },
    {
        id: 'sticker', type: 'DEBIT', title: 'Платежный стикер',
        text: 'Клейте на смартфон и платите как раньше. Бесплатно.',
        rules: (inc: number, pdn: number) => (inc > 40000 ? 40 : 10)
    },

    // === ИНВЕСТИЦИИ ===
    {
        id: 'invest_shares', type: 'INVEST', title: 'Инвестиции: Акции',
        text: 'Готовые портфели российских акций.',
        rules: (inc: number, pdn: number) => (inc > 90000 && pdn < 35 ? 60 : 0)
    },
    {
        id: 'alfa_vklad', type: 'DEBIT', title: 'Альфа-Вклад',
        text: 'Максимальная ставка до 16% годовых.',
        rules: (inc: number, pdn: number) => (inc > 50000 ? 35 : 25)
    },

    // === СТРАХОВАНИЕ ===
    {
        id: 'ins_life', type: 'DEBIT', title: 'Страхование жизни',
        text: 'Защита здоровья и финансовая безопасность семьи.',
        rules: (inc: number, pdn: number) => (inc > 80000 && pdn > 40 ? 55 : 0)
    },
    {
        id: 'base_card', type: 'DEBIT', title: 'Альфа-Карта',
        text: 'Суперкэшбэк каждый месяц. Бесплатное обслуживание.',
        rules: (inc: number, pdn: number) => 5 // База
    }
];

const getSmartOffers = (inc: number, pdn: number) => {
    return PRODUCT_CATALOG
        .map(p => ({ ...p, score: p.rules(inc, pdn) }))
        .filter(p => p.score > 0)
        .sort((a, b) => b.score - a.score)
        .slice(0, 4)
        .map(({ score, rules, ...rest }) => rest)
}

// --- ГРАФИКИ ---
const chartData = computed(() => {
  if (!displayData.value) return { labels: [], datasets: [] }
  const factors = displayData.value.factors.slice(0, 15)
  return {
    labels: factors.map((f: any) => getFeatureName(f.name)),
    datasets: [{
      label: 'Влияние (RUB)',
      data: factors.map((f: any) => f.value),
      backgroundColor: factors.map((f: any) => f.value > 0 ? '#22c55e' : '#ef4444'),
      borderRadius: 4,
      barThickness: 15
    }]
  }
})

const chartOptions = {
  indexAxis: 'y' as const,
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: true, color: 'rgba(0,0,0,0.05)' } },
    y: { grid: { display: false }, ticks: { color: '#6b7280', font: { size: 11 } } }
  }
}

// --- ЛОГИКА ---
onMounted(async () => {
  try {
    const id = route.params.id as string
    data.value = await apiClient.getPrediction(id)
  } catch (e) {
    error.value = true
  } finally {
    setTimeout(() => loading.value = false, 500)
  }
})

const handleSimulation = (changes: any) => {
  if (!data.value) return
  if (!changes) {
    simulatedData.value = null
    return
  }
  const base = JSON.parse(JSON.stringify(data.value))

  // 1. Доход
  const incomeMult = 1 + (changes.incomeChange / 100)
  base.prediction.value = Math.max(0, Math.round(base.prediction.value * incomeMult))

  // 2. ПДН
  const debtMult = 1 + (changes.debtChange / 100)
  const expenseMult = 1 + (changes.expensesChange / 100)
  base.business_metrics.pdn = Math.round(base.business_metrics.pdn * debtMult * expenseMult / incomeMult)
  base.business_metrics.pdn = Math.min(100, Math.max(0, base.business_metrics.pdn))

  // 3. Сегменты
  const inc = base.prediction.value
  const pdn = base.business_metrics.pdn

  if (inc > 150000) base.business_metrics.segment = 'Premium'
  else if (inc > 80000) base.business_metrics.segment = 'Middle'
  else base.business_metrics.segment = 'Mass'

  if (pdn > 50) base.business_metrics.risk_level = 'high'
  else if (pdn < 30) base.business_metrics.risk_level = 'low'
  else base.business_metrics.risk_level = 'medium'

  // 4. Умные офферы (Front-end)
  base.offers = getSmartOffers(inc, pdn)
  simulatedData.value = base
}

const displayData = computed(() => simulatedData.value || data.value)
const refresh = () => window.location.reload()

// --- PDF ГЕНЕРАТОР ---
const generateReport = () => {
  pdfLoading.value = true
  const element = document.getElementById('pdf-report-content')

  const opt = {
    margin: 0,
    filename: `Alfa_Dossier_${route.params.id}.pdf`,
    image: { type: 'jpeg', quality: 0.98 },
    html2canvas: { scale: 2, useCORS: true, scrollY: 0, x: 0, y: 0 },
    jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
  }

  html2pdf().set(opt).from(element).save().then(() => {
    pdfLoading.value = false
    show('Досье успешно сформировано', 'success')
  }).catch((err: any) => {
    console.error(err)
    pdfLoading.value = false
    show('Ошибка при создании PDF', 'error')
  })
}
</script>

<template>
  <div class="animate-fade-in-up pb-10">
    <div v-if="loading" class="flex justify-center h-[60vh] items-center"><div class="animate-spin rounded-full h-12 w-12 border-4 border-[#EF3124] border-t-transparent"></div></div>
    <div v-else-if="error" class="text-center mt-20 text-gray-500">Сервис временно недоступен</div>

    <div v-else-if="displayData">
      <header class="flex flex-col md:flex-row md:justify-between md:items-end mb-8 gap-4">
        <div>
          <h1 class="text-3xl font-bold text-[#0B1F35] flex items-center gap-3 dark:text-white">
            Клиент #{{ route.params.id }}
            <CheckBadgeIcon class="w-6 h-6 text-blue-500" />
          </h1>
          <p class="text-sm text-gray-500 mt-1 dark:text-gray-400">Финансовый скоринг</p>
        </div>
        <div class="flex gap-2">
            <button @click="generateReport" :disabled="pdfLoading" class="flex items-center gap-2 px-4 py-2 bg-[#EF3124] text-white rounded-xl shadow-lg shadow-red-500/30 hover:bg-[#D92D20] transition disabled:opacity-70 font-medium text-sm">
                <span v-if="pdfLoading" class="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full"></span>
                <DocumentArrowDownIcon v-else class="w-5 h-5" />
                {{ pdfLoading ? 'Формирование...' : 'Скачать досье' }}
            </button>
            <div class="bg-gray-100 p-1 rounded-xl flex dark:bg-white/10">
                <button @click="isDetailedMode = false" class="px-4 py-2 rounded-lg text-sm font-medium transition-all" :class="!isDetailedMode ? 'bg-white shadow-sm text-[#0B1F35] dark:bg-gray-700 dark:text-white' : 'text-gray-500 dark:text-gray-400'">Графики</button>
                <button @click="isDetailedMode = true" class="px-4 py-2 rounded-lg text-sm font-medium transition-all" :class="isDetailedMode ? 'bg-white shadow-sm text-[#0B1F35] dark:bg-gray-700 dark:text-white' : 'text-gray-500 dark:text-gray-400'">Таблица</button>
            </div>
        </div>
      </header>

      <div class="grid grid-cols-12 gap-6">
        <div class="col-span-12 lg:col-span-7 space-y-6">
           <Income3DCard :amount="displayData.prediction.value" :confidence="0" />
           <SimulatorPanel :initial-data="{}" @update="handleSimulation" />
           <div class="bg-white/80 backdrop-blur-md p-6 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10">
              <h3 class="font-bold text-[#0B1F35] mb-6 dark:text-white">Факторы влияния (SHAP)</h3>
              <div v-if="!isDetailedMode" class="h-[400px]"><Bar :data="chartData" :options="chartOptions" /></div>
              <div v-else class="space-y-3 max-h-[400px] overflow-y-auto custom-scrollbar pr-2">
                 <div v-for="factor in displayData.factors" :key="factor.name" class="flex justify-between items-center text-sm py-2 border-b border-gray-100 dark:border-white/10">
                    <span class="text-gray-600 dark:text-gray-300 w-1/2 truncate" :title="factor.name">{{ getFeatureName(factor.name) }}</span>
                    <span class="font-mono font-bold" :class="factor.value > 0 ? 'text-green-600' : 'text-red-500'">{{ factor.value > 0 ? '+' : '' }}{{ Math.round(factor.value).toLocaleString() }}</span>
                 </div>
              </div>
           </div>
        </div>

        <div class="col-span-12 lg:col-span-5 space-y-6">
            <div class="grid grid-cols-2 gap-4">
                <div class="bg-white/80 p-5 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10 transition-all duration-300">
                    <div class="text-gray-400 text-xs uppercase font-bold">ПДН (Нагрузка)</div>
                    <div class="text-2xl font-bold mt-1" :class="displayData.business_metrics.pdn > 50 ? 'text-red-500' : 'text-green-500'">{{ displayData.business_metrics.pdn }}%</div>
                </div>
                <div class="bg-white/80 p-5 rounded-2xl shadow-sm border border-white/60 dark:bg-white/5 dark:border-white/10 transition-all duration-300">
                    <div class="text-gray-400 text-xs uppercase font-bold">Сегмент</div>
                    <div class="text-2xl font-bold mt-1 text-[#0B1F35] dark:text-white capitalize">{{ displayData.business_metrics.segment }}</div>
                </div>
            </div>
            <div>
                <h3 class="font-bold text-[#0B1F35] mb-4 flex items-center gap-2 dark:text-white">
                    <BriefcaseIcon class="w-5 h-5 text-[#EF3124]" /> Рекомендации
                    <span v-if="simulatedData" class="text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full animate-pulse font-bold">Simulated</span>
                </h3>
                <transition-group name="list" tag="div" class="space-y-3">
                    <div v-for="offer in displayData.offers" :key="offer.id" class="bg-white/80 p-5 rounded-2xl border border-white/60 shadow-sm hover:border-[#EF3124]/50 transition-all cursor-pointer group dark:bg-white/5 dark:border-white/10">
                        <div class="flex items-start gap-4">
                            <div class="p-3 rounded-full bg-red-50 text-[#EF3124] group-hover:scale-110 transition-transform dark:bg-white/10">
                                <CreditCardIcon v-if="offer.type === 'CREDIT_CARD'" class="w-6 h-6" />
                                <ChartBarIcon v-else-if="offer.type === 'INVEST'" class="w-6 h-6" />
                                <HomeIcon v-else-if="offer.type === 'MORTGAGE'" class="w-6 h-6" />
                                <BanknotesIcon v-else-if="offer.type === 'CASH_LOAN' || offer.type === 'INSTALLMENT'" class="w-6 h-6" />
                                <ArrowPathIcon v-else-if="offer.type === 'REFINANCE'" class="w-6 h-6" />
                                <ShieldCheckIcon v-else-if="offer.type === 'INSURANCE'" class="w-6 h-6" />
                                <DevicePhoneMobileIcon v-else-if="offer.title.includes('Детская') || offer.title.includes('стикер')" class="w-6 h-6" />
                                <BriefcaseIcon v-else class="w-6 h-6" />
                            </div>
                            <div>
                                <div class="font-bold text-[#0B1F35] dark:text-white">{{ offer.title }}</div>
                                <p class="text-xs text-gray-500 mt-1 leading-relaxed dark:text-gray-400">{{ offer.text }}</p>
                            </div>
                        </div>
                    </div>
                </transition-group>
            </div>
        </div>
      </div>
    </div>

    <!-- PDF ШАБЛОН -->
    <div style="position: fixed; top: 0; left: 0; width: 0; height: 0; overflow: hidden; z-index: -1;">
        <div id="pdf-report-content" class="pdf-template-box" v-if="displayData">
            <div class="pdf-content">
                <div class="pdf-header">
                    <div class="pdf-logo">АО «АЛЬФА-БАНК»</div>
                    <div class="pdf-date">Дата: {{ new Date().toLocaleDateString() }}</div>
                </div>
                <h1 class="pdf-title">КРЕДИТНОЕ ДОСЬЕ</h1>
                <div class="pdf-section">
                    <div class="pdf-row"><span class="pdf-label">Клиент ID:</span><span class="pdf-value">{{ route.params.id }}</span></div>
                    <div class="pdf-row"><span class="pdf-label">Сегмент:</span><span class="pdf-value" style="text-transform: uppercase;">{{ displayData.business_metrics.segment }}</span></div>
                </div>
                <div class="pdf-result-box">
                    <div class="pdf-result-label">Скор. Доход</div>
                    <div class="pdf-result-value">{{ displayData.prediction.value.toLocaleString() }} ₽</div>
                    <div class="pdf-result-sub">ПДН: {{ displayData.business_metrics.pdn }}% | Риск: {{ displayData.business_metrics.risk_level.toUpperCase() }}</div>
                </div>
                <h2 class="pdf-subtitle">Факторы риска (SHAP)</h2>
                <table class="pdf-table">
                    <thead><tr><th style="text-align: left">Параметр</th><th style="text-align: right;">Вклад (₽)</th></tr></thead>
                    <tbody>
                        <tr v-for="factor in displayData.factors.slice(0, 10)" :key="factor.name">
                            <td>{{ getFeatureName(factor.name) }}</td>
                            <td style="text-align: right;" :style="{ color: factor.value > 0 ? '#16a34a' : '#dc2626' }">{{ factor.value > 0 ? '+' : '' }}{{ Math.round(factor.value).toLocaleString() }}</td>
                        </tr>
                    </tbody>
                </table>
                <h2 class="pdf-subtitle" style="margin-top: 15px;">Продукты</h2>
                <div class="pdf-offers">
                    <div v-for="offer in displayData.offers.slice(0, 3)" :key="offer.id" class="pdf-offer-item">
                        <div class="pdf-offer-title">{{ offer.title }}</div>
                        <div class="pdf-offer-text">{{ offer.text }}</div>
                    </div>
                </div>
            </div>
            <div class="pdf-footer">Документ сформирован автоматически системой Alfa AI Scoring System.<br>Конфиденциально. Только для внутреннего пользования.</div>
        </div>
    </div>

  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: #ccc; border-radius: 4px; }
.list-move, .list-enter-active, .list-leave-active { transition: all 0.5s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(30px); }
.list-leave-active { position: absolute; }

/* FLEXBOX PDF STYLES */
.pdf-template-box {
    width: 210mm;
    height: 296mm;
    background: white;
    padding: 12mm 15mm;
    color: #000;
    font-family: 'Arial', sans-serif;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-sizing: border-box;
    overflow: hidden;
}
.pdf-content { flex-grow: 1; }
.pdf-header { display: flex; justify-content: space-between; border-bottom: 2px solid #EF3124; padding-bottom: 5px; margin-bottom: 15px; font-size: 11px; }
.pdf-logo { font-weight: bold; color: #EF3124; }
.pdf-title { font-size: 18px; font-weight: bold; text-align: center; margin-bottom: 15px; color: #0B1F35; }
.pdf-section { margin-bottom: 10px; }
.pdf-row { display: flex; justify-content: space-between; margin-bottom: 4px; border-bottom: 1px dotted #ccc; font-size: 11px; }
.pdf-label { color: #666; }
.pdf-value { font-weight: bold; }
.pdf-result-box { background: #f3f4f6; padding: 10px; border-radius: 6px; text-align: center; margin-bottom: 15px; border: 1px solid #ddd; }
.pdf-result-label { font-size: 10px; color: #666; text-transform: uppercase; }
.pdf-result-value { font-size: 22px; font-weight: bold; margin: 5px 0; color: #0B1F35; }
.pdf-result-sub { font-size: 10px; color: #666; }
.pdf-subtitle { font-size: 13px; font-weight: bold; border-left: 3px solid #EF3124; padding-left: 8px; margin-bottom: 8px; color: #0B1F35; }
.pdf-table { width: 100%; border-collapse: collapse; font-size: 10px; }
.pdf-table th, .pdf-table td { border-bottom: 1px solid #eee; padding: 3px; }
.pdf-table th { text-align: left; border-bottom: 1px solid #000; font-weight: bold; }
.pdf-offer-item { margin-bottom: 6px; padding: 6px; border: 1px solid #eee; border-radius: 4px; }
.pdf-offer-title { font-weight: bold; font-size: 11px; color: #0B1F35; }
.pdf-offer-text { font-size: 9px; color: #555; }
.pdf-footer { font-size: 9px; color: #999; text-align: center; border-top: 1px solid #eee; padding-top: 10px; margin-top: auto; }
</style>