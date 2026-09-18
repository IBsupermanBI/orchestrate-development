# Focused validation

Before implementation, identify a few observable outcome scenarios: the primary success case, a material blocked/invalid case, and recovery/error behavior when relevant. Reuse project tests and patterns. Test-first is useful for reproducible defects, security, concurrency, data integrity and fragile public contracts; it is not ceremony for ordinary work.

Workers run the smallest meaningful focused combination of targeted tests, static checks and runtime checks. Root schedules stage validation only after stable integration. Treat failed assertions, non-zero exits, type/build/lint failures where required, exceptions, timeouts and absent expected runtime signals as failures. If a meaningful check cannot run, say so rather than calling it a pass.
