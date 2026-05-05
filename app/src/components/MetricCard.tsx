import { ReactNode } from "react";
import { motion } from "framer-motion";

type MetricCardProps = {
  label: string;
  value: string;
  helper?: string;
  icon?: ReactNode;
};

export function MetricCard({ label, value, helper, icon }: MetricCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45 }}
      whileHover={{ y: -4, scale: 1.01 }}
      className="glass-panel rounded-[1.75rem] p-5"
    >
      <div className="mb-5 flex items-center justify-between">
        <p className="text-xs uppercase tracking-[0.32em] text-slate-400">{label}</p>
        {icon ? (
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl border border-white/10 bg-white/5 text-cyan-300">
            {icon}
          </div>
        ) : null}
      </div>
      <p className="text-3xl font-semibold tracking-tight text-white">{value}</p>
      {helper ? <p className="mt-3 text-sm leading-6 text-slate-400">{helper}</p> : null}
    </motion.div>
  );
}
