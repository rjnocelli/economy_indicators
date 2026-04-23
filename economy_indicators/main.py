from src.pipeline.pipeline import run_pipeline
from src.features.build_features import run_feature_pipeline


if __name__ == "__main__":
    run_pipeline()
    run_feature_pipeline()
