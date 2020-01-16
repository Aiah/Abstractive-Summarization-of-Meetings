import texar.tf as tx

beam_width = 5
hidden_dim = 768

bert = {
    'pretrained_model_name': 'bert-base-uncased'
}

# See https://texar.readthedocs.io/en/latest/code/modules.html#texar.tf.modules.BERTEncoder.default_hparams
bert_encoder = {}

# From https://github.com/asyml/texar/blob/413e07f859acbbee979f274b52942edd57b335c1/examples/transformer/config_model.py#L27-L45
# with adjustments for BERT
decoder = {
    "dim": hidden_dim,
    'num_blocks': 6,
    'multihead_attention': {
        'num_heads': 8,
        'output_dim': hidden_dim
    },
    'initializer': {
        'type': 'variance_scaling_initializer',
        'kwargs': {
            'scale': 1.0,
            'mode': 'fan_avg',
            'distribution': 'uniform',
        },
    },
    'poswise_feedforward': tx.modules.default_transformer_poswise_net_hparams(output_dim=hidden_dim)
}

loss_label_confidence = 0.9

opt = {
    'optimizer': {
        'type': 'AdamOptimizer',
        'kwargs': {
            'beta1': 0.9,
            'beta2': 0.997,
            'epsilon': 1e-9
        }
    }
}

lr = {
    'learning_rate_schedule': 'constant.linear_warmup.rsqrt_decay.rsqrt_depth',
    'lr_constant': 2 * (hidden_dim ** -0.5),
    'static_lr': 1e-3,
    'warmup_steps': 5000,
}
