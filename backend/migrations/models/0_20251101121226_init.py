from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "characters" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "channel_id" VARCHAR(100) NOT NULL,
    "character_name" VARCHAR(255) NOT NULL,
    "image_path" VARCHAR(500) NOT NULL,
    "metadata" JSONB,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_characters_channel_4e96d4" ON "characters" ("channel_id");
COMMENT ON TABLE "characters" IS 'Character model for video generation.';
CREATE TABLE IF NOT EXISTS "generation_jobs" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "video_id" INT NOT NULL,
    "job_id" VARCHAR(255) NOT NULL UNIQUE,
    "status" VARCHAR(50) NOT NULL DEFAULT 'pending',
    "progress" INT NOT NULL DEFAULT 0,
    "error_message" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_generation__video_i_831d9e" ON "generation_jobs" ("video_id");
COMMENT ON TABLE "generation_jobs" IS 'Background generation job tracking.';
CREATE TABLE IF NOT EXISTS "sources" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "filename" VARCHAR(255) NOT NULL,
    "file_type" VARCHAR(20) NOT NULL,
    "file_path" VARCHAR(500),
    "file_size" INT,
    "content" TEXT NOT NULL,
    "summary" TEXT,
    "status" VARCHAR(50) NOT NULL DEFAULT 'pending',
    "error_message" TEXT,
    "language" VARCHAR(10) NOT NULL DEFAULT 'en',
    "page_count" INT,
    "word_count" INT NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS "idx_sources_status_84c6b8" ON "sources" ("status");
COMMENT ON TABLE "sources" IS 'Source document model - COMPLETE FIELDS.';
CREATE TABLE IF NOT EXISTS "videos" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "description" TEXT,
    "duration" INT NOT NULL DEFAULT 60,
    "channel_id" VARCHAR(100) NOT NULL DEFAULT 'research_papers',
    "category_name" VARCHAR(200),
    "category_metadata" JSONB,
    "characters_used" JSONB,
    "custom_prompt" TEXT,
    "prompt_config" VARCHAR(50),
    "status" VARCHAR(50) NOT NULL DEFAULT 'pending',
    "progress" INT NOT NULL DEFAULT 0,
    "error_message" TEXT,
    "output_path" VARCHAR(500),
    "thumbnail_path" VARCHAR(500),
    "script_path" VARCHAR(500),
    "generation_time" DOUBLE PRECISION,
    "file_size" INT,
    "quality_score" DOUBLE PRECISION NOT NULL DEFAULT 0,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completed_at" TIMESTAMPTZ
);
CREATE INDEX IF NOT EXISTS "idx_videos_title_b1ecc7" ON "videos" ("title");
CREATE INDEX IF NOT EXISTS "idx_videos_channel_4264d0" ON "videos" ("channel_id");
CREATE INDEX IF NOT EXISTS "idx_videos_status_068cc9" ON "videos" ("status");
COMMENT ON COLUMN "videos"."channel_id" IS 'research_papers|space_exploration|brainrot_grandfather|brainrot_stories|kids_brainrot';
COMMENT ON TABLE "videos" IS 'Video database model - LOCAL STORAGE ONLY.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
)
