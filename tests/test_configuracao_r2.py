"""Verifica a barreira de configuração usando apenas valores fictícios, sem rede."""

import importlib.util
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import Mock, patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "atualizar_cache_r2.py"


class ConfiguracaoR2Tests(unittest.TestCase):
    def carregar(self):
        self.client = Mock()
        boto3 = types.ModuleType("boto3")
        boto3.client = self.client
        botocore = types.ModuleType("botocore")
        config = types.ModuleType("botocore.config")
        config.Config = Mock()
        with patch.dict(sys.modules, {"boto3": boto3, "botocore": botocore, "botocore.config": config}):
            spec = importlib.util.spec_from_file_location("cache_r2_test", SCRIPT)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        return module

    def test_importar_nao_inicializa_cliente(self):
        with patch.dict(os.environ, {}, clear=True):
            self.carregar()
        self.client.assert_not_called()

    def test_configuracao_ausente_interrompe_antes_do_cliente(self):
        module = self.carregar()
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, "R2_SECRET_ACCESS_KEY"):
                module.criar_cliente_s3()
        self.client.assert_not_called()

    def test_erro_nao_exibe_valores_parciais(self):
        module = self.carregar()
        fake = "valor-ficticio-que-nao-deve-aparecer"
        with patch.dict(os.environ, {"R2_SECRET_ACCESS_KEY": fake}, clear=True):
            with self.assertRaises(ValueError) as ctx:
                module.criar_cliente_s3()
        self.assertNotIn(fake, str(ctx.exception))
        self.client.assert_not_called()

    def test_cliente_usa_ambiente_e_bucket_explicitos(self):
        module = self.carregar()
        values = {"R2_ACCOUNT_ID": "conta-teste", "R2_ACCESS_KEY_ID": "acesso-teste",
                  "R2_SECRET_ACCESS_KEY": "segredo-ficticio", "R2_BUCKET_NAME": "bucket-teste"}
        with patch.dict(os.environ, values, clear=True):
            client, bucket = module.criar_cliente_s3()
        self.assertIs(client, self.client.return_value)
        self.assertEqual(bucket, "bucket-teste")
        args, kwargs = self.client.call_args
        self.assertEqual(args, ("s3",))
        self.assertEqual(kwargs["endpoint_url"], "https://conta-teste.r2.cloudflarestorage.com")
        self.assertEqual(kwargs["aws_access_key_id"], "acesso-teste")
        self.assertEqual(kwargs["aws_secret_access_key"], "segredo-ficticio")


if __name__ == "__main__":
    unittest.main()
