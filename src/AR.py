
class AutoregressiveModel(nn.Module):
    def __init__(self, max_seq_len=50, d_model=64, n_heads=4, n_layers=2):
        super().__init__()
        self.max_seq_len = max_seq_len
        self.d_model = d_model
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        self.input_embedding = nn.Linear(9, d_model)
        self.pos_encoding = nn.Parameter(torch.randn(max_seq_len, d_model) * 0.1)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=n_heads, 
            batch_first=True,
            dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_layers)
        self.output = nn.Linear(d_model, 3)
        self.to(self.device)

    def _generate_causal_mask(self, seq_len):
        """Generate causal mask to prevent looking at future positions"""
        mask = torch.triu(torch.ones(seq_len, seq_len), diagonal=1)
        mask = mask.masked_fill(mask == 1, float('-inf'))
        return mask
    
    def forward(self, x):
        batch_size, seq_len = x.size(0), x.size(1)
        x = self.input_embedding(x)
        x = x + self.pos_encoding[:seq_len].unsqueeze(0)
        causal_mask = self._generate_causal_mask(seq_len).to(x.device)
        transformed = self.transformer(x, mask=causal_mask)
        return self.output(transformed)

    def encode_history(self, my_moves, opp_moves, results):
        """Convert game history to model input format"""
        if len(my_moves) == 0:
            return None
            
        # Limit sequence length
        if len(my_moves) > self.max_seq_len:
            my_moves = my_moves[-self.max_seq_len:]
            opp_moves = opp_moves[-self.max_seq_len:]
            results = results[-self.max_seq_len:]
        
        # One-hot encode everything
        seq_len = len(my_moves)
        encoded = torch.zeros(seq_len, 9)
        
        for i in range(seq_len):
            # One-hot my move
            encoded[i, my_moves[i]] = 1
            # One-hot opponent move  
            encoded[i, 3 + opp_moves[i]] = 1
            # One-hot result (-1, 0, 1 -> 0, 1, 2)
            result_idx = int(results[i]) + 1
            encoded[i, 6 + result_idx] = 1
            
        return encoded.unsqueeze(0).to(self.device)

    def train_step(self, batch_data, optimizer, criterion):
        """Single training step"""
        self.train()
        total_loss = 0
        num_examples = 0
        
        for my_moves, opp_moves, results in batch_data:
            if len(my_moves) < 2:
                continue
                
            # Encode sequence
            input_encoded = self.encode_history(my_moves, opp_moves, results)
            if input_encoded is None:
                continue
            
            # Get predictions for all positions
            optimizer.zero_grad()
            logits = self.forward(input_encoded)
            
            # Create targets: predict moves 1,2,3... from history 0,1,2...
            seq_len = len(my_moves)
            if seq_len > 1:
                targets = torch.tensor(my_moves[1:]).to(self.device)
                predictions = logits[0, :-1, :]  # Skip last prediction (no target)
                
                loss = criterion(predictions, targets)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
                num_examples += len(targets)
        
        return total_loss, num_examples

    def train_model(self, training_data, epochs=50, learning_rate=0.001, batch_size=32):
        """Train the model on game history data"""
        print(f"Training model for {epochs} epochs...")
        
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)
        criterion = nn.CrossEntropyLoss()
        
        for epoch in range(epochs):
            # Shuffle and batch data
            np.random.shuffle(training_data)
            batches = [training_data[i:i+batch_size] for i in range(0, len(training_data), batch_size)]
            
            epoch_loss = 0
            epoch_examples = 0
            
            for batch in batches:
                loss, examples = self.train_step(batch, optimizer, criterion)
                epoch_loss += loss
                epoch_examples += examples
            
            if (epoch + 1) % 10 == 0:
                avg_loss = epoch_loss / max(epoch_examples, 1)
                print(f"Epoch {epoch+1}: Loss = {avg_loss:.4f} ({epoch_examples} examples)")
        
        self.eval()
        print("Training complete!")

    def sample(self, x, temperature=1.0):
        """Sample next move from the model"""
        self.eval()
        with torch.no_grad():
            logits = self.forward(x)
            probs = F.softmax(logits[0, -1, :] / temperature, dim=-1)
            return torch.multinomial(probs, 1).item()

    def save_model(self, path):
        """Save the trained model"""
        torch.save(self.state_dict(), path)
        print(f"Model saved to {path}")
    
    def load_model(self, path):
        """Load a pre-trained model"""
        self.load_state_dict(torch.load(path, map_location=self.device))
        print(f"Model loaded from {path}")