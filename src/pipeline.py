from pathlib import Path
import subprocess
import sys
import time


def run_module(module_name: str) -> None:
    """Execute a Python module and stop if it fails."""

    print("\n" + "=" * 75)
    print(f"RUNNING: {module_name}")
    print("=" * 75)

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

    print(f"\nCompleted: {module_name}")
    print(f"Execution time: {elapsed_time:.2f} seconds")


PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Execute modules in dependency order.
PIPELINE_MODULES = [
    # Data preparation and quality
    "src.prepare_data",
    "src.data_quality",
    "src.data_quality_checks",
    "src.data_quality_report",

    # Sales and product analysis
    "src.exploratory_data_analysis",
    "src.monthly_sales_analysis",
    "src.product_sales_analysis",

    # Customer analysis
    "src.inspect_customer_data",
    "src.customer_purchase_frequency",
    "src.customer_spending_analysis",
    "src.rfm_analysis",
    "src.rfm_scoring",
    "src.customer_segmentation",
    "src.customer_segmentation_visualization",

    # Market basket analysis
    "src.prepare_market_basket",
    "src.build_market_basket_matrix",
    "src.market_basket_analysis",
    "src.enhance_market_basket_report",
    "src.validate_market_basket_rules",
]


def main() -> None:
    """Run the currently implemented analytics workflow."""

    print("=" * 75)
    print("RETAIL CUSTOMER INTELLIGENCE — ANALYTICS PIPELINE")
    print("=" * 75)

    print(f"\nProject directory: {PROJECT_ROOT}")
    print(f"Python executable: {sys.executable}")

    pipeline_start = time.time()

    try:
        for module_name in PIPELINE_MODULES:
            run_module(module_name)

    except RuntimeError as error:
        print("\n" + "!" * 75)
        print("PIPELINE FAILED")
        print(str(error))
        print("!" * 75)
        raise SystemExit(1)

    elapsed_time = time.time() - pipeline_start

    print("\n" + "=" * 75)
    print("CURRENT ANALYTICS PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 75)

    print(f"Total execution time: {elapsed_time:.2f} seconds")

    print("\nNote:")
    print(
        "This version orchestrates the currently implemented modules. "
        "Clustering, forecasting, standardized final outputs, and the "
        "remaining acceptance criteria will be integrated and validated "
        "in subsequent steps."
    )


if __name__ == "__main__":
    main()