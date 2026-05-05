type SectionTitleProps = {
  eyebrow: string;
  title: string;
  description: string;
};

export function SectionTitle({ eyebrow, title, description }: SectionTitleProps) {
  return (
    <div className="mb-8 max-w-4xl md:mb-10">
      <p className="mb-3 text-xs uppercase tracking-[0.38em] text-cyan-300">{eyebrow}</p>
      <h2 className="mb-4 text-3xl font-semibold leading-tight text-white md:text-5xl">{title}</h2>
      <p className="max-w-3xl text-base leading-8 text-slate-300">{description}</p>
    </div>
  );
}
