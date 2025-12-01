// src/pages/NDVIPage.tsx

import React, { useEffect, useState } from "react";
import { LineChart, Activity } from "lucide-react";
import { useLocation } from "../hooks/useLocation";
import LocationInput from "../components/LocationInput";
import ModuleCalculationCard from "../components/ModuleCalculationCard";
import LoadingSpinner from "../components/LoadingSpinner";
import { api } from "../services/api";

export const NDVIPage: React.FC = () => {
  const { location, setLocation } = useLocation();

  // allow flexible API response shape for NDVI analysis
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [analysisData, setAnalysisData] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let mounted = true;
    const fetchAnalysis = async () => {
      if (!location) {
        setAnalysisData(null);
        return;
      }
      setLoading(true);
      try {
        const resp = await api.ndvi.analyze(location.lat, location.lng);
        if (mounted) setAnalysisData(resp);
      } catch {
        if (mounted) setAnalysisData(null);
      } finally {
        if (mounted) setLoading(false);
      }
    };

    fetchAnalysis();
    return () => {
      mounted = false;
    };
  }, [location]);

  // Support multiple backend shapes:
  // - aggregated report: analysisData.ndvi_report (rich object)
  // - microservice flat response: { ndvi_value, health_status, vegetation_coverage, timestamp, trend }
  const ndvi =
    analysisData?.ndvi_report ||
    (analysisData?.ndvi
      ? {
          latestValue:
            typeof analysisData.ndvi.mean === "number" &&
            Number.isFinite(analysisData.ndvi.mean)
              ? analysisData.ndvi.mean
              : null,
          latestDate: analysisData.analysis_date,
          status: analysisData.health_analysis?.status ?? "Unknown",
          trend:
            analysisData.trend_analysis?.summary ||
            analysisData.trend_analysis?.trend ||
            "No trend available",
          change:
            typeof analysisData.ndvi.mean === "number" &&
            typeof analysisData.ndvi.median === "number"
              ? Number(
                  (analysisData.ndvi.mean - analysisData.ndvi.median).toFixed(3)
                )
              : null,
          seasonalAverage:
            typeof analysisData.ndvi.mean === "number" &&
            Number.isFinite(analysisData.ndvi.mean)
              ? analysisData.ndvi.mean
              : null,
          history: Array.isArray(analysisData.ndvi_history)
            ? analysisData.ndvi_history
            : [],
        }
      : analysisData && typeof analysisData.ndvi_value === "number"
      ? {
          // flat NDVI microservice response
          latestValue: Number.isFinite(analysisData.ndvi_value)
            ? analysisData.ndvi_value
            : null,
          latestDate:
            analysisData.timestamp || analysisData.analysis_date || null,
          status:
            analysisData.health_status ?? analysisData.status ?? "Unknown",
          trend: Array.isArray(analysisData.trend)
            ? analysisData.trend
            : analysisData.trend || "No trend available",
          change: null,
          seasonalAverage: Number.isFinite(analysisData.ndvi_value)
            ? analysisData.ndvi_value
            : null,
          history: Array.isArray(analysisData.trend)
            ? (analysisData.trend as { date?: string; value?: number }[]).map(
                (t) => ({
                  date: t.date,
                  value: typeof t.value === "number" ? t.value : undefined,
                })
              )
            : [],
        }
      : null);

  const vegetationCover = Number.isFinite(analysisData?.vegetation_coverage)
    ? analysisData!.vegetation_coverage
    : Number.isFinite(analysisData?.vegetation_percentage)
    ? analysisData!.vegetation_percentage
    : null;

  if (loading) {
    return (
      <div className="space-y-6 text-center py-8">
        <LoadingSpinner />
        <p className="text-gray-600 mt-2">Fetching NDVI analysis…</p>
      </div>
    );
  }

  if (!ndvi) {
    // If user hasn't set a location yet, show the LocationInput so they can pick one
    if (!location) {
      return (
        <div className="py-6">
          <LocationInput
            onLocationSelect={(loc) => {
              // set the location in context which will trigger the NDVI fetch
              try {
                setLocation(loc);
              } catch {
                // ignore
              }
            }}
          />
        </div>
      );
    }

    return (
      <div className="text-center py-12">
        <Activity className="w-16 h-16 mx-auto text-gray-400 mb-4" />
        <p className="text-gray-600 dark:text-gray-400">
          No NDVI data available. Analyze a location to see vegetation health
          metrics.
        </p>
      </div>
    );
  }

  // status coloring removed (unused) — keep simple textual status in UI

  return (
    <div className="space-y-6">
      <section className="bg-white dark:bg-gray-900 rounded-xl p-6">
        <div className="flex items-start space-x-4 mb-6">
          <LineChart className="w-8 h-8 text-gray-700 dark:text-gray-200" />
          <div>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">
              NDVI Analysis
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Normalized Difference Vegetation Index tracks crop health through
              satellite imagery
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <ModuleCalculationCard
            title="Latest NDVI"
            description={
              Number.isFinite(ndvi.latestValue)
                ? `${ndvi.latestValue.toFixed(3)} — ${
                    ndvi.latestDate
                      ? new Date(ndvi.latestDate).toLocaleDateString()
                      : "Date unknown"
                  }`
                : "No recent NDVI available"
            }
          />

          <ModuleCalculationCard
            title="Vegetation Coverage"
            description={
              Number.isFinite(vegetationCover)
                ? `${vegetationCover}% green biomass`
                : "Coverage data not available"
            }
          />

          <ModuleCalculationCard
            title="Seasonal Average"
            description={
              Number.isFinite(ndvi.seasonalAverage)
                ? `${ndvi.seasonalAverage.toFixed(3)} — ${
                    ndvi.change !== null
                      ? ((ndvi.change / ndvi.seasonalAverage) * 100).toFixed(
                          2
                        ) + "%"
                      : "Change N/A"
                  }`
                : "No seasonal average"
            }
          />
        </div>

        {/* NDVI Trend Chart */}
        {ndvi.history && ndvi.history.length > 0 && (
          <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
              NDVI Trend Over Time
            </h3>
          </div>
        )}

        {/* Status Summary */}
        <div className="bg-linear-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 rounded-xl p-6 border border-green-200 dark:border-green-800">
          <h4 className="font-semibold text-gray-900 dark:text-white mb-2">
            Current Status: {ndvi.status}
          </h4>
          <p className="text-gray-700 dark:text-gray-300">{ndvi.trend}</p>
        </div>
      </section>
    </div>
  );
};

export default NDVIPage;
