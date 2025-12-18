import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface HealthBadgeProps {
    score: number;
    status: string;
    className?: string;
    showLabel?: boolean;
    size?: "sm" | "md" | "lg";
}

export function HealthBadge({ score, status, className, showLabel = true, size = "md" }: HealthBadgeProps) {
    let colorClass = "bg-gray-500";

    const sizeClasses = {
        sm: "px-2 py-0.5 text-xs",
        md: "px-3 py-1 text-sm font-bold",
        lg: "px-4 py-2 text-base font-bold",
    };

    if (score >= 70) {
        colorClass = "bg-green-500 hover:bg-green-600";
    } else if (score >= 40) {
        colorClass = "bg-yellow-500 hover:bg-yellow-600";
    } else {
        colorClass = "bg-red-500 hover:bg-red-600";
    }

    return (
        <Badge className={cn(colorClass, "text-white", sizeClasses[size], className)}>
            {score} {showLabel && `/ 100 (${status.replace("_", " ").toUpperCase()})`}
        </Badge>
    );
}
