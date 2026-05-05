import { useEffect, useMemo, useState } from "react";
import { Link, NavLink, Route, Routes } from "react-router-dom";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  ArrowRight,
  BarChart3,
  BrainCircuit,
  ChevronRight,
  CloudCog,
  Database,
  LayoutDashboard,
  Search,
  ShieldCheck,
  Sparkles,
  TrendingUp,
  Users,
} from "lucide-react";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { MetricCard } from "./components/MetricCard";
import { SectionTitle } from "./components/SectionTitle";
import { formatCurrency, formatDecimal, formatPercent } from "./lib/format";

type Metrics = {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
  baseline_churn_rate: number;
  threshold_used: number;
  tradeoff_summary: string;
};

type Prediction = {
  cliente_id: string;
  nome: string;
  estado: string;
  perfil_risco: string;
  origem_dado?: string;
  renda_mensal: number;
  saldo_atual: number;
  prob_churn: number;
  predicao_churn: number;
  risco: "Baixo" | "Medio" | "Alto";
  recomendacao: string;
};

type Feature = {
  feature: string;
  importance: number;
};

type Summary = {
  total_clientes: number;
  total_transacoes: number;
  churn_rate_real: number;
  ticket_medio: number;
  volume_total: number;
  top_categorias_consumo: { nome_categoria: string; valor: number }[];
  evolucao_mensal: { ano_mes: string; valor: number }[];
  risk_distribution: { name: string; value: number }[];
  avg_prob_by_state: { estado: string; prob_churn: number }[];
  impact: {
    clientes_alto_risco: number;
    clientes_medio_risco: number;
    clientes_baixo_risco: number;
    ticket_medio_clientes_alto_risco: number;
    share_clientes_alto_risco: number;
  };
  frontend_notes: {
    premium_free: string;
    aws_ready: string;
    data_foundation: string;
  };
  data_source_type: string;
  data_source_name: string;
  data_source_platform: string;
  data_source_file: string;
  public_dataset_used: boolean;
  synthetic_transactions_used: boolean;
  data_source_note: string;
};

const navItems = [
  { to: "/", label: "Landing" },
  { to: "/dashboard", label: "Dashboard Executivo" },
  { to: "/clientes-risco", label: "Clientes em Risco" },
  { to: "/ml-insights", label: "ML Insights" },
  { to: "/arquitetura", label: "Arquitetura" },
  { to: "/power-bi-guide", label: "Power BI Guide" },
];

const COLORS = {
  cyan: "#22d3ee",
  violet: "#8b5cf6",
  lilac: "#c084fc",
  rose: "#fb7185",
  white: "#f8fafc",
};

const defaultMetrics: Metrics = {
  accuracy: 0,
  precision: 0,
  recall: 0,
  f1_score: 0,
  roc_auc: 0,
  baseline_churn_rate: 0,
  threshold_used: 0,
  tradeoff_summary: "Os artefatos do modelo ainda nao foram carregados. Rode o pipeline para atualizar as metricas.",
};

const defaultSummary: Summary = {
  total_clientes: 0,
  total_transacoes: 0,
  churn_rate_real: 0,
  ticket_medio: 0,
  volume_total: 0,
  top_categorias_consumo: [],
  evolucao_mensal: [],
  risk_distribution: [],
  avg_prob_by_state: [],
  impact: {
    clientes_alto_risco: 0,
    clientes_medio_risco: 0,
    clientes_baixo_risco: 0,
    ticket_medio_clientes_alto_risco: 0,
    share_clientes_alto_risco: 0,
  },
  frontend_notes: {
    premium_free: "Os arquivos do frontend ainda nao foram carregados.",
    aws_ready: "Rode o pipeline e gere os JSONs antes da apresentacao.",
    data_foundation: "Dados indisponiveis no momento.",
  },
  data_source_type: "unknown",
  data_source_name: "Nao carregado",
  data_source_platform: "Local",
  data_source_file: "app/public/data/summary.json",
  public_dataset_used: false,
  synthetic_transactions_used: false,
  data_source_note: "Os JSONs do frontend estao ausentes ou vazios. Rode o pipeline para reconstruir os artefatos.",
};

async function fetchJson<T>(path: string, fallback: T): Promise<T> {
  try {
    const response = await fetch(path);
    if (!response.ok) {
      return fallback;
    }
    const text = await response.text();
    if (!text.trim()) {
      return fallback;
    }
    return JSON.parse(text) as T;
  } catch {
    return fallback;
  }
}

function App() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]);
  const [featureImportance, setFeatureImportance] = useState<Feature[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);

  useEffect(() => {
    async function loadData() {
      const [loadedMetrics, loadedPredictions, loadedFeatures, loadedSummary] = await Promise.all([
        fetchJson<Metrics>("/data/metrics.json", defaultMetrics),
        fetchJson<Prediction[]>("/data/predictions.json", []),
        fetchJson<Feature[]>("/data/feature_importance.json", []),
        fetchJson<Summary>("/data/summary.json", defaultSummary),
      ]);
      setMetrics(loadedMetrics);
      setPredictions(loadedPredictions);
      setFeatureImportance(loadedFeatures);
      setSummary(loadedSummary);
    }
    void loadData();
  }, []);

  if (!metrics || !summary) {
    return (
      <div className="flex min-h-screen items-center justify-center text-slate-300">
        <div className="glass-panel rounded-3xl px-8 py-6 text-center">
          <p className="mb-2 text-xs uppercase tracking-[0.38em] text-cyan-300">Aurora</p>
          <p className="text-lg text-white">Carregando Aurora Finance Intelligence...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen">
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -left-24 top-0 h-72 w-72 rounded-full bg-cyan-400/10 blur-3xl" />
        <div className="absolute right-0 top-28 h-80 w-80 rounded-full bg-violet-500/10 blur-3xl" />
        <div className="absolute bottom-0 left-1/3 h-72 w-72 rounded-full bg-fuchsia-400/10 blur-3xl" />
      </div>

      <header className="sticky top-0 z-40 border-b border-white/10 bg-[#081120]/70 backdrop-blur-2xl">
        <div className="mx-auto max-w-7xl px-4 py-4 sm:px-6">
          <div className="flex items-center justify-between gap-6">
            <Link to="/" className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-300 shadow-[0_0_40px_rgba(34,211,238,0.16)]">
                <Sparkles size={18} />
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.34em] text-slate-400">Aurora</p>
                <p className="text-sm font-medium text-white">Finance Intelligence</p>
              </div>
            </Link>

            <nav className="hidden rounded-full border border-white/10 bg-white/5 px-3 py-2 lg:flex lg:gap-1">
              {navItems.map((item) => (
                <NavLink
                  key={item.to}
                  to={item.to}
                  className={({ isActive }) =>
                    `rounded-full px-4 py-2 text-sm transition ${
                      isActive ? "bg-white/10 text-white" : "text-slate-300 hover:bg-white/5 hover:text-white"
                    }`
                  }
                >
                  {item.label}
                </NavLink>
              ))}
            </nav>
          </div>

          <nav className="mt-4 flex gap-2 overflow-x-auto pb-1 lg:hidden">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `whitespace-nowrap rounded-full border px-4 py-2 text-sm transition ${
                    isActive
                      ? "border-cyan-300/40 bg-cyan-300/10 text-cyan-100"
                      : "border-white/10 bg-white/5 text-slate-300"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="relative z-10 mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10">
        <Routes>
          <Route path="/" element={<Landing metrics={metrics} summary={summary} predictions={predictions} />} />
          <Route
            path="/dashboard"
            element={<ExecutiveDashboard metrics={metrics} summary={summary} predictions={predictions} />}
          />
          <Route path="/clientes-risco" element={<RiskClientsPage predictions={predictions} />} />
          <Route
            path="/ml-insights"
            element={<MlInsightsPage metrics={metrics} featureImportance={featureImportance} />}
          />
          <Route path="/arquitetura" element={<ArchitecturePage summary={summary} />} />
          <Route path="/power-bi-guide" element={<PowerBiGuidePage />} />
        </Routes>
      </main>
    </div>
  );
}

function Landing({
  metrics,
  summary,
  predictions,
}: {
  metrics: Metrics;
  summary: Summary;
  predictions: Prediction[];
}) {
  const highRisk = predictions.filter((item) => item.risco === "Alto").length;

  return (
    <div className="space-y-10 md:space-y-14">
      <section className="grid gap-8 xl:grid-cols-[1.18fr_0.82fr] xl:items-stretch">
        <motion.div
          initial={{ opacity: 0, y: 24 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55 }}
          className="glass-panel relative overflow-hidden rounded-[2rem] p-8 sm:p-10"
        >
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.14),transparent_26%),radial-gradient(circle_at_80%_20%,rgba(139,92,246,0.16),transparent_28%)]" />
          <div className="relative">
            <div className="mb-6 flex flex-wrap gap-3">
              {["Python", "SQL", "Power BI", "Machine Learning", "AWS-ready"].map((chip) => (
                <span
                  key={chip}
                  className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs uppercase tracking-[0.24em] text-slate-200"
                >
                  {chip}
                </span>
              ))}
            </div>
            <p className="mb-4 text-xs uppercase tracking-[0.42em] text-cyan-300">Fintech intelligence · premium free</p>
            <h1 className="aurora-title mb-6 max-w-4xl text-5xl font-semibold leading-[1.02] md:text-6xl xl:text-7xl">
              Aurora Finance Intelligence
            </h1>
            <p className="max-w-3xl text-lg leading-8 text-slate-300">
              Dados que antecipam riscos, revelam padrões e apoiam decisões financeiras mais humanas. Um MVP de churn
              intelligence com cara de produto real, pronto para banca, Power BI e deploy estático.
            </p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link
                to="/dashboard"
                className="inline-flex items-center gap-2 rounded-full bg-cyan-300 px-6 py-3 text-sm font-semibold text-slate-950 shadow-[0_18px_50px_rgba(34,211,238,0.25)]"
              >
                Explorar Dashboard
                <ArrowRight size={16} />
              </Link>
              <Link
                to="/arquitetura"
                className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/5 px-6 py-3 text-sm font-medium text-white"
              >
                Ver Arquitetura
                <ChevronRight size={16} />
              </Link>
            </div>
            <div className="mt-10 grid gap-4 md:grid-cols-3">
              <MetricStrip label="Clientes" value={summary.total_clientes.toLocaleString("pt-BR")} />
              <MetricStrip label="ROC-AUC" value={formatDecimal(metrics.roc_auc, 4)} />
              <MetricStrip label="Alto risco" value={highRisk.toLocaleString("pt-BR")} />
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 18 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.55, delay: 0.08 }}
          className="grid gap-5"
        >
          <div className="glass-panel rounded-[2rem] p-7">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.34em] text-slate-400">Executive Pulse</p>
                <h3 className="mt-2 text-2xl font-semibold text-white">Resumo estratégico</h3>
              </div>
              <div className="rounded-2xl border border-cyan-300/20 bg-cyan-300/10 p-3 text-cyan-200">
                <TrendingUp size={18} />
              </div>
            </div>
            <div className="space-y-5">
              <InsightRow label="Volume total transacionado" value={formatCurrency(summary.volume_total)} />
              <InsightRow label="Ticket médio da base" value={formatCurrency(summary.ticket_medio)} />
              <InsightRow label="Taxa de churn simulada" value={formatPercent(summary.churn_rate_real)} />
            </div>
          </div>

          <div className="glass-panel rounded-[2rem] p-7">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-[0.34em] text-slate-400">Risk Snapshot</p>
                <h3 className="mt-2 text-2xl font-semibold text-white">Distribuição de risco</h3>
              </div>
              <div className="rounded-2xl border border-violet-300/20 bg-violet-300/10 p-3 text-violet-200">
                <BarChart3 size={18} />
              </div>
            </div>
            <div className="space-y-4">
              {summary.risk_distribution.map((item) => (
                <div key={item.name}>
                  <div className="mb-2 flex items-center justify-between text-sm text-slate-300">
                    <span>{item.name}</span>
                    <span>{item.value.toLocaleString("pt-BR")}</span>
                  </div>
                  <div className="h-2 rounded-full bg-white/5">
                    <div
                      className="h-2 rounded-full"
                      style={{
                        width: `${(item.value / summary.total_clientes) * 100}%`,
                        background:
                          item.name === "Alto"
                            ? "linear-gradient(90deg,#fb7185,#f43f5e)"
                            : item.name === "Medio"
                              ? "linear-gradient(90deg,#22d3ee,#38bdf8)"
                              : "linear-gradient(90deg,#8b5cf6,#c084fc)",
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>
      </section>

      <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        {[
          {
            title: "Pipeline confiável",
            body: "Simulação, limpeza, EDA, features e inferência com a mesma base de verdade.",
            icon: <Database size={18} />,
          },
          {
            title: "SQL aplicável",
            body: "Consultas prontas para olhar churn, canal, risco, gasto e recência com contexto de negócio.",
            icon: <LayoutDashboard size={18} />,
          },
          {
            title: "Storytelling executivo",
            body: "App e Power BI preparados para apresentar risco com clareza, leitura visual e narrativa.",
            icon: <Sparkles size={18} />,
          },
          {
            title: "Arquitetura sem atrito",
            body: "Frontend estático e AWS-ready, sem exigir backend, banco cloud ou custo recorrente.",
            icon: <CloudCog size={18} />,
          },
        ].map((item, index) => (
          <motion.div
            key={item.title}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.45, delay: index * 0.06 }}
            className="glass-panel rounded-[1.75rem] p-6"
          >
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-200">
              {item.icon}
            </div>
            <h3 className="mb-3 text-xl font-semibold text-white">{item.title}</h3>
            <p className="text-sm leading-7 text-slate-300">{item.body}</p>
          </motion.div>
        ))}
      </section>
    </div>
  );
}

function ExecutiveDashboard({
  metrics,
  summary,
  predictions,
}: {
  metrics: Metrics;
  summary: Summary;
  predictions: Prediction[];
}) {
  const altoRisco = predictions.filter((item) => item.risco === "Alto").length;
  const medioRisco = predictions.filter((item) => item.risco === "Medio").length;

  return (
    <div className="space-y-8">
      <SectionTitle
        eyebrow="Dashboard Executivo"
        title="Uma leitura premium de risco, churn e oportunidade"
        description="Os principais números do modelo, da base financeira e do impacto potencial de retenção em um dashboard com cara de SaaS."
      />

      <div className="inline-flex rounded-full border border-cyan-300/20 bg-cyan-300/10 px-4 py-2 text-sm text-cyan-50">
        {summary.public_dataset_used
          ? "Base publica Kaggle + camada sintetica de transacoes"
          : "Fallback sintetico ativo + camada sintetica de transacoes"}
      </div>

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          label="Total de clientes"
          value={summary.total_clientes.toLocaleString("pt-BR")}
          helper="Base analítica ativa"
          icon={<Users size={18} />}
        />
        <MetricCard
          label="Taxa de churn"
          value={formatPercent(summary.churn_rate_real)}
          helper="Churn real da base simulada"
          icon={<AlertTriangle size={18} />}
        />
        <MetricCard label="ROC-AUC" value={formatDecimal(metrics.roc_auc, 4)} helper="Capacidade de ranking" icon={<BrainCircuit size={18} />} />
        <MetricCard
          label="Precision"
          value={formatDecimal(metrics.precision, 4)}
          helper="Threshold otimizado para retenção"
          icon={<ShieldCheck size={18} />}
        />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.18fr_0.82fr]">
        <ChartCard
          title="Evolução mensal do volume financeiro"
          subtitle="Últimos meses da base simulada"
          accent="cyan"
        >
          <ResponsiveContainer width="100%" height={320}>
            <AreaChart data={summary.evolucao_mensal}>
              <defs>
                <linearGradient id="volumeGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#22d3ee" stopOpacity={0.55} />
                  <stop offset="100%" stopColor="#22d3ee" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
              <XAxis dataKey="ano_mes" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <YAxis tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <Tooltip contentStyle={tooltipStyle} />
              <Area type="monotone" dataKey="valor" stroke="#22d3ee" fill="url(#volumeGradient)" strokeWidth={3} />
            </AreaChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Distribuição de risco" subtitle="Visão rápida da carteira" accent="violet">
          <div className="grid h-full gap-4 lg:grid-cols-[0.9fr_1.1fr] lg:items-center">
            <div className="h-72">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie data={summary.risk_distribution} dataKey="value" nameKey="name" innerRadius={72} outerRadius={108}>
                    {summary.risk_distribution.map((entry) => (
                      <Cell
                        key={entry.name}
                        fill={entry.name === "Alto" ? COLORS.rose : entry.name === "Medio" ? COLORS.cyan : COLORS.violet}
                      />
                    ))}
                  </Pie>
                  <Tooltip contentStyle={tooltipStyle} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="space-y-4">
              <RiskSummaryCard label="Alto risco" value={altoRisco} color="bg-rose-400" helper="prioridade máxima" />
              <RiskSummaryCard label="Médio risco" value={medioRisco} color="bg-cyan-400" helper="engajamento ativo" />
              <RiskSummaryCard
                label="Baixo risco"
                value={summary.total_clientes - altoRisco - medioRisco}
                color="bg-violet-400"
                helper="monitoramento leve"
              />
            </div>
          </div>
        </ChartCard>
      </div>

      <div className="grid gap-6 xl:grid-cols-[1fr_1fr]">
        <ChartCard title="Top categorias de consumo" subtitle="Volume transacionado por categoria" accent="cyan">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={summary.top_categorias_consumo}>
              <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
              <XAxis dataKey="nome_categoria" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <YAxis tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="valor" fill="#22d3ee" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <ChartCard title="Risco médio por estado" subtitle="Top UFs com maior propensão média" accent="violet">
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={summary.avg_prob_by_state}>
              <CartesianGrid stroke="rgba(148,163,184,0.12)" vertical={false} />
              <XAxis dataKey="estado" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <YAxis tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="prob_churn" fill="#8b5cf6" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>

      <div className="glass-panel rounded-[2rem] p-7">
        <div className="mb-6 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.34em] text-cyan-300">Impacto de negócio</p>
            <h3 className="mt-2 text-3xl font-semibold text-white">O score como ferramenta de decisão</h3>
          </div>
          <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300">
            alto risco = {formatPercent(summary.impact.share_clientes_alto_risco)}
          </div>
        </div>
        <div className="grid gap-5 lg:grid-cols-[1fr_0.95fr]">
          <div className="grid gap-4 sm:grid-cols-2">
            <ValuePanel label="Volume total da base" value={formatCurrency(summary.volume_total)} helper="carteira observada" />
            <ValuePanel
              label="Ticket médio do alto risco"
              value={formatCurrency(summary.impact.ticket_medio_clientes_alto_risco)}
              helper="potencial sensível"
            />
            <ValuePanel label="Alto risco" value={altoRisco.toLocaleString("pt-BR")} helper="retenção prioritária" />
            <ValuePanel
              label="Threshold do modelo"
              value={formatDecimal(metrics.threshold_used, 2)}
              helper="ajuste operacional"
            />
          </div>
          <div className="rounded-[1.5rem] border border-cyan-300/20 bg-cyan-300/10 p-5 text-sm leading-7 text-cyan-50">
            A Aurora foi desenhada para apoiar decisão humana. O foco do MVP não é automatizar ações finais, e sim
            ordenar a fila certa de clientes, revelar vulnerabilidades com antecedência e dar contexto para a equipe de
            retenção agir melhor.
          </div>
        </div>
      </div>
    </div>
  );
}

function RiskClientsPage({ predictions }: { predictions: Prediction[] }) {
  const [search, setSearch] = useState("");
  const [risk, setRisk] = useState<"Todos" | "Baixo" | "Medio" | "Alto">("Todos");

  const filtered = useMemo(() => {
    return predictions.filter((item) => {
      const byRisk = risk === "Todos" ? true : item.risco === risk;
      const bySearch =
        item.cliente_id.toLowerCase().includes(search.toLowerCase()) ||
        item.nome.toLowerCase().includes(search.toLowerCase());
      return byRisk && bySearch;
    });
  }, [predictions, risk, search]);

  return (
    <div className="space-y-8">
      <SectionTitle
        eyebrow="Clientes em Risco"
        title="Uma mesa de priorização pronta para retenção"
        description="Busca rápida, filtros claros e uma tabela com leitura executiva para a equipe decidir quem merece atenção agora."
      />

      <div className="grid gap-5 md:grid-cols-3">
        <ValuePanel
          label="Clientes listados"
          value={filtered.length.toLocaleString("pt-BR")}
          helper="resultado após filtros"
        />
        <ValuePanel
          label="Maior probabilidade"
          value={filtered[0] ? formatPercent(filtered[0].prob_churn) : "0%"}
          helper="top da fila atual"
        />
        <ValuePanel label="Filtro ativo" value={risk} helper="segmentação por faixa" />
      </div>

      <div className="glass-panel rounded-[2rem] p-5 sm:p-6">
        <div className="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between">
          <div className="relative w-full max-w-xl">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500" size={18} />
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Buscar por cliente_id ou nome"
              className="w-full rounded-2xl border border-white/10 bg-white/5 px-12 py-3 text-white outline-none transition focus:border-cyan-300/40 focus:bg-white/10"
            />
          </div>
          <div className="flex flex-wrap gap-2">
            {["Todos", "Baixo", "Medio", "Alto"].map((item) => (
              <button
                key={item}
                onClick={() => setRisk(item as "Todos" | "Baixo" | "Medio" | "Alto")}
                className={`rounded-full px-4 py-2 text-sm transition ${
                  risk === item
                    ? "bg-cyan-300 text-slate-950 shadow-[0_10px_30px_rgba(34,211,238,0.25)]"
                    : "border border-white/10 bg-white/5 text-slate-300 hover:bg-white/10"
                }`}
              >
                {item}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="glass-panel overflow-hidden rounded-[2rem]">
        <div className="overflow-x-auto">
          <table className="min-w-[1100px] w-full text-left">
            <thead className="sticky top-0 border-b border-white/10 bg-[#0f172a]/90 text-xs uppercase tracking-[0.22em] text-slate-400 backdrop-blur-xl">
              <tr>
                {["Cliente", "Prob. churn", "Risco", "Renda", "Perfil", "Estado", "Recomendação"].map((head) => (
                  <th key={head} className="px-5 py-4 font-medium">
                    {head}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.slice(0, 120).map((item, index) => (
                <motion.tr
                  key={item.cliente_id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.22, delay: Math.min(index * 0.015, 0.2) }}
                  className="border-b border-white/5 text-sm text-slate-200 transition hover:bg-white/[0.03]"
                >
                  <td className="px-5 py-4">
                    <div>
                      <p className="font-medium text-white">{item.cliente_id}</p>
                      <p className="mt-1 text-xs text-slate-400">{item.nome}</p>
                    </div>
                  </td>
                  <td className="px-5 py-4 font-medium text-white">{formatPercent(item.prob_churn)}</td>
                  <td className="px-5 py-4">
                    <RiskBadge risco={item.risco} />
                  </td>
                  <td className="px-5 py-4">{formatCurrency(item.renda_mensal)}</td>
                  <td className="px-5 py-4">{item.perfil_risco}</td>
                  <td className="px-5 py-4">{item.estado}</td>
                  <td className="px-5 py-4 text-slate-300">
                    <div className="max-w-md leading-6">{item.recomendacao}</div>
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

function MlInsightsPage({ metrics, featureImportance }: { metrics: Metrics; featureImportance: Feature[] }) {
  return (
    <div className="space-y-8">
      <SectionTitle
        eyebrow="ML Insights"
        title="Leitura visual do modelo e dos trade-offs"
        description="Uma camada didática para explicar desempenho, threshold e importância de variáveis sem perder a estética de produto premium."
      />

      <div className="grid gap-5 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard label="Accuracy" value={formatDecimal(metrics.accuracy, 4)} helper="visão geral" icon={<BarChart3 size={18} />} />
        <MetricCard label="Precision" value={formatDecimal(metrics.precision, 4)} helper="menos falsos positivos" icon={<ShieldCheck size={18} />} />
        <MetricCard label="Recall" value={formatDecimal(metrics.recall, 4)} helper="mais sensível à retenção" icon={<AlertTriangle size={18} />} />
        <MetricCard label="Threshold" value={formatDecimal(metrics.threshold_used, 2)} helper="ajuste operacional" icon={<BrainCircuit size={18} />} />
      </div>

      <div className="grid gap-6 xl:grid-cols-[1.08fr_0.92fr]">
        <ChartCard title="Feature importance" subtitle="Sinais mais relevantes do Random Forest" accent="cyan">
          <ResponsiveContainer width="100%" height={420}>
            <BarChart data={[...featureImportance].reverse()} layout="vertical" margin={{ left: 20 }}>
              <CartesianGrid stroke="rgba(148,163,184,0.12)" horizontal={false} />
              <XAxis type="number" tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <YAxis dataKey="feature" type="category" width={180} tick={{ fill: "#cbd5e1", fontSize: 12 }} />
              <Tooltip contentStyle={tooltipStyle} />
              <Bar dataKey="importance" fill="#22d3ee" radius={[0, 10, 10, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        <div className="space-y-6">
          <div className="glass-panel rounded-[2rem] p-6">
            <h3 className="mb-3 text-xl font-semibold text-white">Random Forest em contexto</h3>
            <p className="text-sm leading-7 text-slate-300">
              O modelo combina várias árvores de decisão para capturar relações não lineares entre renda, saldo,
              recência, mix de consumo e intensidade de crédito. Em um MVP de churn, ele oferece um equilíbrio muito bom
              entre robustez analítica e legibilidade de negócio.
            </p>
          </div>
          <div className="glass-panel rounded-[2rem] p-6">
            <h3 className="mb-3 text-xl font-semibold text-white">Precision vs Recall</h3>
            <p className="text-sm leading-7 text-slate-300">{metrics.tradeoff_summary}</p>
            <div className="mt-4 rounded-[1.5rem] border border-violet-300/20 bg-violet-300/10 p-4 text-sm leading-7 text-violet-50">
              O MVP prioriza ranking de risco. Isso significa que a Aurora ajuda a montar a fila de retenção, mas a
              decisão final continua humana, contextual e responsável.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ArchitecturePage({ summary }: { summary: Summary }) {
  const flow = [
    { title: "Dados Brutos", detail: "clientes, categorias, transações" },
    { title: "Pipeline Python", detail: "simulação, limpeza, features" },
    { title: "EDA & SQL", detail: "estatística, figuras, segmentação" },
    { title: "Modelo ML", detail: "Random Forest + threshold" },
    { title: "Artefatos", detail: "CSV, JSON, model.pkl" },
    { title: "Power BI", detail: "painel executivo" },
    { title: "App + AWS Static", detail: "frontend premium free" },
  ];

  return (
    <div className="space-y-8">
      <SectionTitle
        eyebrow="Arquitetura"
        title="Uma arquitetura bonita, objetiva e sem custo obrigatório"
        description="A Aurora foi desenhada para parecer produto de verdade, mas com a simplicidade operacional ideal para hackathon e demo executiva."
      />

      <div className="glass-panel rounded-[1.5rem] px-5 py-4 text-sm leading-7 text-slate-300">
        <span className="font-medium text-white">Fundação de dados:</span> {summary.frontend_notes.data_foundation}
      </div>

      <div className="glass-panel rounded-[1.5rem] px-5 py-4 text-sm leading-7 text-slate-300">
        <span className="font-medium text-white">Fonte atual:</span> {summary.data_source_name} ({summary.data_source_platform})
        <br />
        <span className="font-medium text-white">Arquivo:</span> {summary.data_source_file}
        <br />
        <span className="font-medium text-white">Nota:</span> {summary.data_source_note}
      </div>

      <div className="glass-panel rounded-[2rem] p-7">
        <div className="mb-6 flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.34em] text-cyan-300">Fluxo principal</p>
            <h3 className="mt-2 text-3xl font-semibold text-white">Do dado bruto ao app estático</h3>
          </div>
          <div className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-300">
            {summary.total_transacoes.toLocaleString("pt-BR")} transações processadas
          </div>
        </div>

        <div className="grid gap-4 lg:grid-cols-7">
          {flow.map((item, index) => (
            <motion.div
              key={item.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.35, delay: index * 0.05 }}
              className="relative rounded-[1.5rem] border border-white/10 bg-white/5 p-5"
            >
              <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-200">
                {index + 1}
              </div>
              <h4 className="text-base font-semibold text-white">{item.title}</h4>
              <p className="mt-2 text-sm leading-6 text-slate-400">{item.detail}</p>
            </motion.div>
          ))}
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-3">
        <ArchitectureFeatureCard
          icon={<CloudCog className="text-cyan-300" />}
          title="Versão premium free"
          body="O frontend consome JSONs estáticos gerados pelo pipeline. Isso reduz risco operacional, acelera a demo e evita dependência de backend."
        />
        <ArchitectureFeatureCard
          icon={<Database className="text-violet-300" />}
          title="Sem backend obrigatório"
          body="Nada depende de API, banco cloud ou serviços pagos. O projeto roda inteiro localmente e pode ser publicado como site estático."
        />
        <ArchitectureFeatureCard
          icon={<ShieldCheck className="text-fuchsia-300" />}
          title="AWS-ready sem susto"
          body="O mesmo app pode ser entregue em S3 Static Website ou Amplify Hosting. O segredo é manter a demo limitada ao build estático."
        />
      </div>
    </div>
  );
}

function PowerBiGuidePage() {
  return (
    <div className="space-y-8">
      <SectionTitle
        eyebrow="Power BI Guide"
        title="Tudo pronto para virar painel executivo"
        description="Quais arquivos importar, como estruturar as páginas e como manter a entrega visual coerente entre BI e app."
      />

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="glass-panel rounded-[2rem] p-6">
          <h3 className="mb-4 text-xl font-semibold text-white">Arquivos para importar</h3>
          <ul className="space-y-3 text-sm leading-7 text-slate-300">
            <li>`dados/processed/base_analitica_clientes.csv`</li>
            <li>`dados/outputs/predicoes_churn.csv`</li>
            <li>`dados/outputs/metricas_modelo.json`</li>
            <li>`dados/outputs/feature_importance.csv`</li>
          </ul>
        </div>
        <div className="glass-panel rounded-[2rem] p-6">
          <h3 className="mb-4 text-xl font-semibold text-white">Páginas sugeridas</h3>
          <ul className="space-y-3 text-sm leading-7 text-slate-300">
            <li>Visão executiva com KPIs e distribuição de risco</li>
            <li>Clientes em alto risco com ações sugeridas</li>
            <li>Leitura do modelo e feature importance</li>
            <li>Segmentação por estado, canal e perfil de risco</li>
          </ul>
        </div>
      </div>

      <div className="glass-panel rounded-[2rem] p-6">
        <h3 className="mb-4 text-xl font-semibold text-white">Medidas DAX sugeridas</h3>
        <pre className="overflow-x-auto rounded-[1.5rem] border border-white/10 bg-black/20 p-5 text-sm text-cyan-100">
{`Clientes = DISTINCTCOUNT(Base[cliente_id])
Churn Rate = AVERAGE(Base[churn_flag])
Clientes Alto Risco =
CALCULATE(COUNTROWS(Predicoes), Predicoes[risco] = "Alto")

Probabilidade Média =
AVERAGE(Predicoes[prob_churn])`}
        </pre>
        <p className="mt-4 text-sm leading-7 text-slate-300">
          Salve os prints finais em `powerbi/screenshots/` para manter evidência visual da camada de BI e reforçar a
          apresentação para a banca.
        </p>
      </div>
    </div>
  );
}

function MetricStrip({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[1.5rem] border border-white/10 bg-white/[0.04] px-5 py-4">
      <p className="text-xs uppercase tracking-[0.24em] text-slate-400">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-white">{value}</p>
    </div>
  );
}

function InsightRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-end justify-between gap-4 border-b border-white/5 pb-4 last:border-b-0 last:pb-0">
      <p className="text-sm text-slate-300">{label}</p>
      <p className="text-lg font-semibold text-white">{value}</p>
    </div>
  );
}

function RiskSummaryCard({
  label,
  value,
  color,
  helper,
}: {
  label: string;
  value: number;
  color: string;
  helper: string;
}) {
  return (
    <div className="rounded-[1.5rem] border border-white/10 bg-white/[0.03] p-4">
      <div className="mb-3 flex items-center justify-between">
        <div className={`h-3 w-3 rounded-full ${color}`} />
        <span className="text-xs uppercase tracking-[0.22em] text-slate-500">{helper}</span>
      </div>
      <p className="text-sm text-slate-300">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-white">{value.toLocaleString("pt-BR")}</p>
    </div>
  );
}

function ValuePanel({ label, value, helper }: { label: string; value: string; helper: string }) {
  return (
    <div className="rounded-[1.5rem] border border-white/10 bg-white/[0.03] p-5">
      <p className="text-xs uppercase tracking-[0.22em] text-slate-500">{label}</p>
      <p className="mt-3 text-2xl font-semibold text-white">{value}</p>
      <p className="mt-2 text-sm text-slate-400">{helper}</p>
    </div>
  );
}

function ChartCard({
  title,
  subtitle,
  accent,
  children,
}: {
  title: string;
  subtitle: string;
  accent: "cyan" | "violet";
  children: React.ReactNode;
}) {
  const accentClass =
    accent === "cyan"
      ? "from-cyan-400/20 to-transparent border-cyan-300/20"
      : "from-violet-400/20 to-transparent border-violet-300/20";

  return (
    <div className={`glass-panel rounded-[2rem] border bg-gradient-to-br ${accentClass} p-6`}>
      <div className="mb-5">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-400">{subtitle}</p>
        <h3 className="mt-2 text-2xl font-semibold text-white">{title}</h3>
      </div>
      {children}
    </div>
  );
}

function RiskBadge({ risco }: { risco: Prediction["risco"] }) {
  const styles =
    risco === "Alto"
      ? "bg-rose-500/15 text-rose-200 border-rose-400/20"
      : risco === "Medio"
        ? "bg-cyan-500/15 text-cyan-200 border-cyan-400/20"
        : "bg-violet-500/15 text-violet-200 border-violet-400/20";

  return <span className={`rounded-full border px-3 py-1 text-xs font-medium ${styles}`}>{risco}</span>;
}

function ArchitectureFeatureCard({
  icon,
  title,
  body,
}: {
  icon: React.ReactNode;
  title: string;
  body: string;
}) {
  return (
    <div className="glass-panel rounded-[2rem] p-6">
      <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/5">
        {icon}
      </div>
      <h3 className="mb-3 text-xl font-semibold text-white">{title}</h3>
      <p className="text-sm leading-7 text-slate-300">{body}</p>
    </div>
  );
}

const tooltipStyle = {
  backgroundColor: "rgba(8, 17, 32, 0.96)",
  border: "1px solid rgba(148, 163, 184, 0.16)",
  borderRadius: "18px",
  color: "#e2e8f0",
};

export default App;
