import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import type { DashboardStats, RiskyAccount } from "@/types/dashboard";
import { dashboardService } from "@/services/dashboardService";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { HealthBadge } from "@/components/health/HealthBadge";
import { ArrowRight, AlertTriangle } from "lucide-react";

export default function Dashboard() {
    const navigate = useNavigate();
    const [stats, setStats] = useState<DashboardStats | null>(null);
    const [riskyAccounts, setRiskyAccounts] = useState<RiskyAccount[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState<string | null>(null);

    useEffect(() => {
        const fetchDashboard = async () => {
            try {
                const [statsData, riskyData] = await Promise.all([
                    dashboardService.getStats(),
                    dashboardService.getRiskyAccounts()
                ]);
                setStats(statsData);
                setRiskyAccounts(riskyData);
            } catch (error) {
                console.error("Dashboard fetch failed:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchDashboard();
    }, []);

    const filteredRisky = riskyAccounts.filter(acc => {
        if (filter === "at_risk") return acc.status === "at_risk";
        return true;
    });

    if (loading) return (
        <div className="flex h-[400px] items-center justify-center p-8">
            <div className="flex flex-col items-center gap-2">
                <Loader2 className="h-8 w-8 animate-spin text-primary" />
                <p className="text-sm text-slate-500 animate-pulse">Orchestrating your portfolio...</p>
            </div>
        </div>
    );

    return (
        <div className="space-y-8 p-8 max-w-7xl mx-auto">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h1 className="text-4xl font-extrabold tracking-tight text-slate-900">Portfolio Dashboard</h1>
                    <p className="text-slate-500 mt-1">Real-time pulse of your customer health and subscription risks.</p>
                </div>
                <div className="flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-full text-xs font-medium text-slate-600">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                    </span>
                    Live Data
                </div>
            </div>

            {/* KPI Cards */}
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
                <Card className="hover:border-primary/50 transition-all shadow-sm border-slate-200/60 bg-white/50 backdrop-blur-sm">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-xs font-bold uppercase tracking-widest text-slate-400">Total Portfolio</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-black text-slate-900">{stats?.total_accounts || 0}</div>
                        <p className="text-[10px] text-slate-400 mt-1">Managed Accounts</p>
                    </CardContent>
                </Card>
                <Card className="hover:border-primary/50 transition-all shadow-sm border-slate-200/60 bg-white/50 backdrop-blur-sm">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-xs font-bold uppercase tracking-widest text-slate-400">Portfolio Health</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-black text-blue-600">{stats?.average_score || 0}%</div>
                        <p className="text-[10px] text-slate-400 mt-1">Aggregate Score</p>
                    </CardContent>
                </Card>
                <Card
                    className={`cursor-pointer transition-all shadow-md border-2 ${filter === "at_risk" ? 'border-red-500 bg-red-50/50 scale-[1.02]' : 'border-slate-200/60 hover:border-red-200 hover:bg-red-50/10'}`}
                    onClick={() => setFilter(filter === "at_risk" ? null : "at_risk")}
                >
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-xs font-bold uppercase tracking-widest text-slate-400 font-mono">Critical Risk</CardTitle>
                        <AlertTriangle className={`h-4 w-4 ${filter === "at_risk" ? 'text-red-600 animate-pulse' : 'text-red-500'}`} />
                    </CardHeader>
                    <CardContent>
                        <div className={`text-3xl font-black ${stats?.health_distribution.at_risk ? 'text-red-600' : 'text-slate-900'}`}>
                            {stats?.health_distribution.at_risk || 0}
                        </div>
                        <p className="text-[10px] text-slate-400 mt-1">{filter === "at_risk" ? "Tap to clear filter" : "Tap to investigate"}</p>
                    </CardContent>
                </Card>
                <Card className="hover:border-primary/50 transition-all shadow-sm border-slate-200/60 bg-white/50 backdrop-blur-sm">
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-xs font-bold uppercase tracking-widest text-slate-400 whitespace-nowrap">Expansion Potential</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-black text-emerald-600">{stats?.health_distribution.healthy || 0}</div>
                        <p className="text-[10px] text-slate-400 mt-1">High-Confidence Accounts</p>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-8 lg:grid-cols-7">
                {/* Risky Accounts List - Takes up 4 columns */}
                <div className="lg:col-span-4 space-y-6">
                    <div className="flex items-center justify-between">
                        <h2 className="text-2xl font-black tracking-tight text-slate-800">
                            {filter === "at_risk" ? "🚨 Priority Recovery" : "Accounts Requiring Attention"}
                        </h2>
                        {filter && (
                            <Button variant="link" size="sm" onClick={() => setFilter(null)} className="text-xs text-red-600 font-bold hover:no-underline">
                                Reset View
                            </Button>
                        )}
                    </div>

                    <div className="grid gap-4">
                        {filteredRisky.length === 0 ? (
                            <Card className="bg-slate-50/50 border-dashed border-2">
                                <CardContent className="py-24 text-center">
                                    <div className="mx-auto w-12 h-12 bg-emerald-100 rounded-full flex items-center justify-center mb-4">
                                        <ArrowRight className="h-6 w-6 text-emerald-600 rotate-[-45deg]" />
                                    </div>
                                    <h3 className="text-lg font-bold text-slate-700">All Clear</h3>
                                    <p className="text-sm text-slate-500">No accounts match your current filter criteria.</p>
                                </CardContent>
                            </Card>
                        ) : (
                            filteredRisky.map((account) => (
                                <Card
                                    key={account.id}
                                    className="group cursor-pointer hover:shadow-2xl hover:-translate-y-1 transition-all duration-300 border-none bg-white ring-1 ring-slate-200/60 overflow-hidden"
                                    onClick={() => navigate(`/accounts/${account.id}`)}
                                >
                                    <div className={`h-1 w-full ${account.status === 'at_risk' ? 'bg-red-500' : 'bg-yellow-400'}`}></div>
                                    <CardHeader className="pb-4 pt-6">
                                        <div className="flex justify-between items-start">
                                            <div className="space-y-1">
                                                <CardTitle className="text-xl group-hover:text-primary transition-colors font-bold">{account.name}</CardTitle>
                                                <div className="flex items-center gap-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
                                                    <span>{account.tier}</span>
                                                    <span>•</span>
                                                    <span>{account.industry || "General"}</span>
                                                </div>
                                            </div>
                                            <HealthBadge score={account.score} status={account.status} size="lg" />
                                        </div>
                                    </CardHeader>
                                    <CardContent className="pb-6">
                                        <div className="flex justify-between items-center bg-slate-50/80 rounded-lg px-4 py-3 group-hover:bg-slate-100 transition-colors">
                                            <span className="text-xs font-bold text-slate-500">NEXT STEPS: Review commitments</span>
                                            <Button variant="ghost" size="sm" className="h-8 w-8 rounded-full p-0">
                                                <ArrowRight className="h-4 w-4" />
                                            </Button>
                                        </div>
                                    </CardContent>
                                </Card>
                            ))
                        )}
                    </div>
                </div>

                {/* Upcoming Renewals - Takes up 3 columns */}
                <div className="lg:col-span-3 space-y-6">
                    <h2 className="text-2xl font-black tracking-tight text-slate-800">Projected Renewals</h2>
                    <Card className="bg-slate-900 text-white border-none shadow-xl overflow-hidden relative group">
                        <div className="absolute top-0 right-0 w-32 h-32 bg-primary/20 blur-3xl -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-700" />
                        <CardHeader>
                            <CardTitle className="text-xs font-bold uppercase tracking-widest text-slate-400">Total ARR at Risk</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="text-4xl font-black">
                                {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(stats?.arr_at_risk || 0)}
                            </div>
                            <p className="text-xs text-slate-400 mt-2 font-medium opacity-80">Next 90 days forecasting</p>
                        </CardContent>
                    </Card>

                    <div className="space-y-4">
                        {stats?.upcoming_renewals && stats.upcoming_renewals.length > 0 ? (
                            stats.upcoming_renewals.map((renewal) => (
                                <div
                                    key={renewal.id}
                                    className="p-5 rounded-2xl border border-slate-100 bg-white hover:border-primary/30 hover:shadow-lg transition-all cursor-pointer relative group"
                                >
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="space-y-1">
                                            <div className="text-base font-bold text-slate-900 group-hover:text-primary transition-colors">{renewal.account_name}</div>
                                            <div className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">{renewal.contract_name}</div>
                                        </div>
                                        <div className="text-base font-black text-slate-900">
                                            {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(renewal.arr)}
                                        </div>
                                    </div>
                                    <div className="flex justify-between items-center text-xs">
                                        <div className="flex items-center gap-2">
                                            <div className={`h-2 w-2 rounded-full ${new Date(renewal.end_date) < new Date(Date.now() + 30 * 24 * 60 * 60 * 1000) ? 'bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.5)]' : 'bg-yellow-500'}`} />
                                            <span className="font-bold text-slate-500">Expires {new Date(renewal.end_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</span>
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="py-12 border-2 border-dashed rounded-2xl flex flex-col items-center justify-center text-slate-400">
                                <span className="text-sm font-medium">No renewals approaching</span>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

const Loader2 = ({ className }: { className?: string }) => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        <path d="M21 12a9 9 0 1 1-6.219-8.56" />
    </svg>
);
