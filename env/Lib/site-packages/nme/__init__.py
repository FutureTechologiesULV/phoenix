import warnings

from local_migrator import (
    class_to_str,
    check_for_errors_in_dkt_values,
    register_class,
    nme_object_hook,
    rename_key,
    MigrationInfo,
    MigrationRegistration,
    NMEEncoder,
    REGISTER,
    update_argument,
    nme_cbor_encoder,
    nme_cbor_decoder,
)

warnings.warn("nme is deprecated, use local_migrator instead", DeprecationWarning)

del warnings

__version__ = "0.1.8"

__all__ = (
    "class_to_str",
    "check_for_errors_in_dkt_values",
    "register_class",
    "nme_object_hook",
    "rename_key",
    "MigrationInfo",
    "MigrationRegistration",
    "NMEEncoder",
    "REGISTER",
    "update_argument",
    "nme_cbor_encoder",
    "nme_cbor_decoder",
    "__version__",
)