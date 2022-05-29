import rx
import rx.operators as ops
import diart.operators as myops
from diart.sources import MicrophoneAudioSource
import diart.functional as fn

sample_rate = 16000
mic = MicrophoneAudioSource(sample_rate=sample_rate)

# Initialize independent modules
segmentation = fn.FrameWiseModel("pyannote/segmentation")
embedding = fn.ChunkWiseModel("pyannote/embedding")
osp = fn.OverlappedSpeechPenalty(gamma=3, beta=10)
normalization = fn.EmbeddingNormalization(norm=1)

# Reformat microphone stream. Defaults to 5s duration and 500ms shift
regular_stream = mic.stream.pipe(myops.regularize_stream(sample_rate=sample_rate))
# Branch the microphone stream to calculate segmentation
segmentation_stream = regular_stream.pipe(ops.map(segmentation))
# Join audio and segmentation stream to calculate speaker embeddings
embedding_stream = rx.zip(regular_stream, segmentation_stream).pipe(
    ops.starmap(lambda wave, seg: (wave, osp(seg))),
    ops.starmap(embedding),
    ops.map(normalization)
)
embedding_stream.__format__()
embedding_stream.subscribe(on_next=lambda emb: print(emb.shape))

mic.read()