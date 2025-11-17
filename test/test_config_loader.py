from job_recommender.src.core.load_config import LoadConfig

def test_load():
    print("=== TEST: LoadConfig ===")

    try:
        cfg = LoadConfig(env="dev")
        print("Loaded config object:")
        print(cfg.config)

        print("\nLogging settings:")
        print("  level   :", cfg.config.logging.level)
        # print("  filepath:", cfg.config.logging.filepath) - if need file


        print("\nConfig path:")
        print(cfg.config_path)

        print("\nSUCCESS: Config loaded without errors.\n")

    except Exception as e:
        print(f"{e}")


