from pathlib import Path
import subprocess
import sys
import time


PROJECT_ROOT = Path(__file__).resolve().parent.parent


PIPELINE_MODULES = [
    # 1. Data preparation and quality
    "src.prepare_data",
    "src.data_quality",
    "src.data_quality_checks",
    "src.data_quality_report",

    # 2. Sales and product analysis
    "src.exploratory_data_analysis",
    "src.monthly_sales_analysis",
    "src.product_sales_analysis",

    # 3. Customer analysis and RFM segmentation
    "src.inspect_customer_data",
    "src.customer_purchase_frequency",
    "src.customer_spending_analysis",
    "src.rfm_analysis",
    "src.rfm_scoring",
    "src.customer_segmentation",
    "src.customer_segmentation_visualization",

    # 4. Market basket analysis
    "src.prepare_market_basket",
    "src.build_market_basket_matrix",
    "src.market_basket_analysis",
    "src.enhance_market_basket_report",
    "src.validate_market_basket_rules",

    # 5. Standardized outputs required by downstream modules
    "src.build_standard_outputs",

    # 6. Customer clustering
    "src.prepare_clustering_data",
    "src.evaluate_clustering",
    "src.fit_customer_clusters",
    "src.visualize_customer_clusters",

    # 7. Monthly sales forecasting
    "src.forecasting",
]


def run_module(module_name: str) -> None:
    """Execute a project module and stop if it fails."""

    print("\n" + "=" * 75, flush=True)
    print(f"RUNNING: {module_name}", flush=True)
    print("=" * 75, flush=True)

    start_time = time.time()

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        cwd=PROJECT_ROOT,
        check=False,
    )

    elapsed_time = time.time() - start_time

    if result.returncode != 0:
        raise RuntimeError(
            f"Pipeline stopped because {module_name} failed "
            f"with exit code {result.returncode}."
        )

    print(
        f"\nCompleted: {module_name} "
        f"({elapsed_time:.2f} seconds)",
        flush=True,
    )


def main() -> None:
    """Run the end-to-end retail analytics workflow."""

    print("=" * 75, flush=True)
    print("RETAIL CUSTOMER INTELLIGENCE - ANALYTICS PIPELINE", flush=True)
    print("=" * 75, flush=True)

    print(f"\nProject directory: {PROJECT_ROOT}", flush=True)
    print(f"Python executable: {sys.executable}", flush=True)

    pipeline_start = time.time()

    try:
        for module_name in PIPELINE_MODULES:
            run_module(module_name)

    except RuntimeError as error:
        print("\n" + "!" * 75, flush=True)
        print("PIPELINE FAILED", flush=True)
        print(str(error), flush=True)
        print("!" * 75, flush=True)
        raise SystemExit(1)

    elapsed_time = time.time() - pipeline_start

    print("\n" + "=" * 75, flush=True)
    print("ANALYTICS PIPELINE COMPLETED SUCCESSFULLY", flush=True)
    print("=" * 75, flush=True)

    print(f"Total execution time: {elapsed_time:.2f} seconds", flush=True)
    print(f"Modules executed: {len(PIPELINE_MODULES)}", flush=True)

    print(
        "\nNote: Forecasting results are baseline comparisons only. "
        "The short historical period does not support reliable "
        "long-term or annual seasonal conclusions.",
        flush=True,
    )


if __name__ == "__main__":
    main()
