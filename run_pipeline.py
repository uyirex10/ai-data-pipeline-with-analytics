from app.pipelines.sales_pipeline import SalesPipeline


def main():

    pipeline = SalesPipeline(
        source_type="csv",
        source_config={
            "file_path": "data/raw/sample_sales.csv"
        }
    )

    pipeline.run()


if __name__ == "__main__":
    main()