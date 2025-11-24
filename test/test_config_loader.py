from src.job_recommender.core.project_config import ProjectConfig

def test_load():
    print("=== TEST: LoadConfig ===")

    try:
        cfg = ProjectConfig(env_provider="dev")
        print("Loaded config object: \n")
        print(cfg.config)

        # print("\nLogging settings:")
        # print("  level   :", cfg.config.logging.level)
        # print("  filepath:", cfg.config.logging.filepath) - if need file

        # print("\nProject:")
        # print("  project   :", cfg.config.app.name)

        print("\nConfig path:")
        print(cfg.config_path)



        print("\nSUCCESS: Config loaded without errors.\n")

    except Exception as e:
        print(f"{e}")


